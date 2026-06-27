from backend.app.repositories.domain_repositories import BookingRepository, ArtistRepository, ServiceRepository, PaymentRepository, UserRepository
from datetime import datetime
import string
import random

class BookingService:
    def __init__(self):
        self.booking_repo = BookingRepository()
        self.artist_repo = ArtistRepository()
        self.service_repo = ServiceRepository()
        self.payment_repo = PaymentRepository()
        self.user_repo = UserRepository()

    def get_available_slots(self, date, artist_id):
        all_slots = ["08:00", "10:00", "13:00", "15:00", "17:00"]
        bookings = self.booking_repo.find_all({
            "date": date,
            "artist_id": artist_id,
            "status": {"$nin": ["cancelled"]}
        })
        booked_times = [b.get("time") for b in bookings]
        return [s for s in all_slots if s not in booked_times]

    def create_booking(self, user_id, artist_id, service_id, date, time, notes):
        artist = self.artist_repo.find_by_id(artist_id)
        service = self.service_repo.find_by_id(service_id)
        user = self.user_repo.find_by_id(user_id)
        
        if not artist or not service or not user:
            return False, "Data tidak valid"
            
        # Check slot availability again
        available = self.get_available_slots(date, artist_id)
        if time not in available:
            return False, "Jadwal sudah terisi, silakan pilih waktu lain."

        code = "BK" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        new_booking = {
            "booking_code": code,
            "customer_name": user.get("fullname"),
            "customer_id": user_id,
            "artist_name": artist.get("name"),
            "artist_id": str(artist["_id"]),
            "service_name": service.get("name"),
            "service_id": str(service["_id"]),
            "service_price": service.get("price"),
            "date": date,
            "time": time,
            "status": "pending",
            "notes": notes,
            "created_at": datetime.now()
        }
        self.booking_repo.insert(new_booking)
        return True, "Booking berhasil dibuat!"

    def get_user_bookings(self, user_id):
        return self.booking_repo.collection.find({"customer_id": user_id}).sort("created_at", -1)

    def upload_payment_proof(self, booking_id, filename):
        booking = self.booking_repo.find_by_id(booking_id)
        if not booking:
            return False, "Booking not found"
            
        self.booking_repo.update(booking_id, {"status": "waiting_payment"})
        self.payment_repo.insert({
            "booking_id": str(booking["_id"]),
            "booking_code": booking.get("booking_code"),
            "customer_name": booking.get("customer_name"),
            "amount": booking.get("service_price"),
            "payment_status": "uploaded",
            "proof_image": filename,
            "created_at": datetime.now()
        })
        return True, "Bukti pembayaran berhasil diupload"
