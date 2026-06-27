from backend.app.database.connection import mongo
from backend.app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(mongo.db.users)

class ArtistRepository(BaseRepository):
    def __init__(self):
        super().__init__(mongo.db.artists)

class BookingRepository(BaseRepository):
    def __init__(self):
        super().__init__(mongo.db.bookings)

class ServiceRepository(BaseRepository):
    def __init__(self):
        super().__init__(mongo.db.services)

class GalleryRepository(BaseRepository):
    def __init__(self):
        super().__init__(mongo.db.gallery)

class PaymentRepository(BaseRepository):
    def __init__(self):
        super().__init__(mongo.db.payments)
