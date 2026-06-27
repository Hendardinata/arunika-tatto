from flask import Blueprint, jsonify, request, session, current_app
import os
from backend.app.middlewares.auth_middleware import login_required, role_required
from backend.app.services.booking_service import BookingService
from backend.app.services.resource_service import ResourceService
from backend.app.repositories.domain_repositories import (
    UserRepository, PaymentRepository, ArtistRepository,
    ServiceRepository, GalleryRepository
)
from backend.app.database.connection import mongo
from bson import ObjectId
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix="/api")
booking_service = BookingService()
resource_service = ResourceService()
user_repo = UserRepository()
payment_repo = PaymentRepository()
artist_repo = ArtistRepository()
service_repo = ServiceRepository()
gallery_repo = GalleryRepository()


def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict."""
    if not doc:
        return None
    result = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)
        elif hasattr(value, "isoformat"):
            result[key] = value.isoformat()
        else:
            result[key] = value
    return result


def serialize_list(cursor):
    return [serialize_doc(doc) for doc in cursor]


# ─── Public GET endpoints ────────────────────────────────────────────────────

@api_bp.route("/artists")
def api_artists():
    limit = int(request.args.get("limit", 0))
    artists = serialize_list(resource_service.get_artists(limit))
    return jsonify({"success": True, "artists": artists})


@api_bp.route("/services")
def api_services():
    limit = int(request.args.get("limit", 0))
    services = serialize_list(resource_service.get_services(limit))
    return jsonify({"success": True, "services": services})


@api_bp.route("/gallery")
def api_gallery():
    limit = int(request.args.get("limit", 0))
    gallery = serialize_list(resource_service.get_gallery(limit))
    return jsonify({"success": True, "gallery": gallery})


@api_bp.route("/slots")
def api_slots():
    date = request.args.get("date")
    artist_id = request.args.get("artist_id")
    if not date or not artist_id:
        return jsonify({"success": False, "slots": []})
    slots = booking_service.get_available_slots(date, artist_id)
    return jsonify({"success": True, "slots": slots})


# ─── Admin: Artists CRUD ─────────────────────────────────────────────────────

@api_bp.route("/artists", methods=["POST"])
@login_required
@role_required("admin")
def api_add_artist():
    data = request.get_json() or {}
    if not data.get("name"):
        return jsonify({"success": False, "message": "Nama artist wajib diisi"}), 400
    new_artist = {
        "name": data.get("name"),
        "specialization": data.get("specialization", ""),
        "experience": data.get("experience", ""),
        "instagram": data.get("instagram", ""),
        "description": data.get("description", ""),
        "status": "active",
        "created_at": datetime.now()
    }
    artist_repo.insert(new_artist)
    return jsonify({"success": True, "message": "Artist berhasil ditambahkan"})


@api_bp.route("/artists/<artist_id>", methods=["DELETE"])
@login_required
@role_required("admin")
def api_delete_artist(artist_id):
    result = artist_repo.delete(artist_id)
    if result:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Artist tidak ditemukan"}), 404


@api_bp.route("/artists/<artist_id>", methods=["PUT"])
@login_required
@role_required("admin")
def api_update_artist(artist_id):
    data = request.get_json() or {}
    if not data.get("name"):
        return jsonify({"success": False, "message": "Nama artist wajib diisi"}), 400
    update_data = {
        "name":           data.get("name"),
        "specialization": data.get("specialization", ""),
        "experience":     data.get("experience", ""),
        "instagram":      data.get("instagram", ""),
        "description":    data.get("description", ""),
        "status":         data.get("status", "active"),
        "updated_at":     datetime.now()
    }
    result = artist_repo.update(artist_id, update_data)
    if result:
        return jsonify({"success": True, "message": "Artist berhasil diupdate"})
    return jsonify({"success": False, "message": "Artist tidak ditemukan"}), 404


# ─── Admin: Services CRUD ────────────────────────────────────────────────────

@api_bp.route("/services", methods=["POST"])
@login_required
@role_required("admin")
def api_add_service():
    data = request.get_json() or {}
    if not data.get("name") or not data.get("price"):
        return jsonify({"success": False, "message": "Nama dan harga wajib diisi"}), 400
    new_service = {
        "name": data.get("name"),
        "price": int(data.get("price", 0)),
        "duration": int(data.get("duration", 0)) if data.get("duration") else None,
        "description": data.get("description", ""),
        "created_at": datetime.now()
    }
    service_repo.insert(new_service)
    return jsonify({"success": True, "message": "Service berhasil ditambahkan"})


@api_bp.route("/services/<service_id>", methods=["DELETE"])
@login_required
@role_required("admin")
def api_delete_service(service_id):
    result = service_repo.delete(service_id)
    if result:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Service tidak ditemukan"}), 404


@api_bp.route("/services/<service_id>", methods=["PUT"])
@login_required
@role_required("admin")
def api_update_service(service_id):
    data = request.get_json() or {}
    if not data.get("name") or not data.get("price"):
        return jsonify({"success": False, "message": "Nama dan harga wajib diisi"}), 400
    update_data = {
        "name":        data.get("name"),
        "price":       int(data.get("price", 0)),
        "duration":    int(data.get("duration")) if data.get("duration") else None,
        "description": data.get("description", ""),
        "updated_at":  datetime.now()
    }
    result = service_repo.update(service_id, update_data)
    if result:
        return jsonify({"success": True, "message": "Service berhasil diupdate"})
    return jsonify({"success": False, "message": "Service tidak ditemukan"}), 404


# ─── Admin: Gallery CRUD ─────────────────────────────────────────────────────

@api_bp.route("/gallery", methods=["POST"])
@login_required
@role_required("admin")
def api_add_gallery():
    title = request.form.get("title")
    artist_id = request.form.get("artist_id")
    category = request.form.get("category", "other")
    file = request.files.get("image")

    if not title:
        return jsonify({"success": False, "message": "Judul karya wajib diisi"}), 400

    image_filename = None
    if file and file.filename:
        upload_folder = current_app.config.get("UPLOAD_FOLDER", "frontend/static/uploads")
        os.makedirs(upload_folder, exist_ok=True)
        image_filename = f"gallery_{int(datetime.now().timestamp())}_{file.filename}"
        file.save(os.path.join(upload_folder, image_filename))

    # Resolve artist name from id
    artist_name = ""
    if artist_id:
        artist = artist_repo.find_by_id(artist_id)
        if artist:
            artist_name = artist.get("name", "")

    new_item = {
        "title": title,
        "artist_id": artist_id,
        "artist_name": artist_name,
        "category": category,
        "image": image_filename,
        "created_at": datetime.now()
    }
    gallery_repo.insert(new_item)
    return jsonify({"success": True, "message": "Karya berhasil ditambahkan"})


@api_bp.route("/gallery/<item_id>", methods=["DELETE"])
@login_required
@role_required("admin")
def api_delete_gallery(item_id):
    result = gallery_repo.delete(item_id)
    if result:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Item tidak ditemukan"}), 404


# ─── Admin: Bookings ─────────────────────────────────────────────────────────

@api_bp.route("/bookings")
@login_required
@role_required("admin")
def api_bookings():
    status_filter = request.args.get("status")
    query = {"status": status_filter} if status_filter else {}
    bookings = serialize_list(booking_service.booking_repo.find_all(query))
    return jsonify({"success": True, "bookings": bookings})


@api_bp.route("/bookings/<booking_id>", methods=["PUT"])
@login_required
@role_required("admin")
def api_update_booking(booking_id):
    data = request.get_json() or {}
    new_status = data.get("status")
    if not new_status:
        return jsonify({"success": False, "message": "Status diperlukan"}), 400
    result = booking_service.booking_repo.update(booking_id, {"status": new_status})
    if result:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Booking tidak ditemukan"}), 404


# ─── Customer: My Bookings ────────────────────────────────────────────────────

@api_bp.route("/my-bookings")
@login_required
def api_my_bookings():
    user_id = session.get("user_id")
    bookings = serialize_list(booking_service.get_user_bookings(user_id))
    return jsonify({"success": True, "bookings": bookings})


# ─── Admin: Payments ─────────────────────────────────────────────────────────

@api_bp.route("/payments")
@login_required
@role_required("admin")
def api_payments():
    payments = serialize_list(payment_repo.find_all())
    return jsonify({"success": True, "payments": payments})


@api_bp.route("/payments/<payment_id>/confirm", methods=["POST"])
@login_required
@role_required("admin")
def api_confirm_payment(payment_id):
    try:
        payment = payment_repo.find_by_id(payment_id)
        if not payment:
            return jsonify({"success": False, "message": "Payment tidak ditemukan"}), 404
        payment_repo.update(payment_id, {
            "payment_status": "confirmed",
            "confirmed_at": datetime.now()
        })
        booking_service.booking_repo.update(
            payment.get("booking_id"), {"status": "confirmed"}
        )
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


# ─── Customer: Upload Payment Proof ──────────────────────────────────────────

@api_bp.route("/payment/upload-proof", methods=["POST"])
@login_required
def api_upload_proof():
    booking_id = request.form.get("booking_id")
    file = request.files.get("proof_image")
    if not booking_id or not file:
        return jsonify({"success": False, "message": "Data tidak lengkap"}), 400

    upload_folder = current_app.config.get("UPLOAD_FOLDER", "frontend/static/uploads")
    os.makedirs(upload_folder, exist_ok=True)
    filename = f"proof_{booking_id}_{int(datetime.now().timestamp())}_{file.filename}"
    file.save(os.path.join(upload_folder, filename))

    success, msg = booking_service.upload_payment_proof(booking_id, filename)
    return jsonify({"success": success, "message": msg})


# ─── Admin: Customers ────────────────────────────────────────────────────────

@api_bp.route("/customers")
@login_required
@role_required("admin")
def api_customers():
    customers = serialize_list(user_repo.find_all({"role": "customer"}))
    return jsonify({"success": True, "customers": customers})


# ─── Admin: Dashboard Stats ──────────────────────────────────────────────────

@api_bp.route("/dashboard/stats")
@login_required
@role_required("admin")
def api_dashboard_stats():
    total_bookings = booking_service.booking_repo.count()
    waiting_payment = booking_service.booking_repo.count({"status": "waiting_payment"})
    completed = booking_service.booking_repo.count({"status": "completed"})

    pipeline = [
        {"$match": {"payment_status": "confirmed"}},
        {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
    ]
    result = list(payment_repo.collection.aggregate(pipeline))
    revenue = result[0]["total"] if result else 0

    return jsonify({
        "success": True,
        "stats": {
            "total_bookings": total_bookings,
            "waiting_payment": waiting_payment,
            "completed": completed,
            "revenue": revenue
        }
    })


# ─── Settings ────────────────────────────────────────────────────────────────

@api_bp.route("/settings", methods=["GET"])
@login_required
@role_required("admin")
def api_get_settings():
    """Retrieve studio settings from the database."""
    doc = mongo.db.settings.find_one({"key": "studio"})
    settings = serialize_doc(doc) if doc else {}
    settings.pop("key", None)  # remove internal key field
    return jsonify({"success": True, "settings": settings})


@api_bp.route("/settings", methods=["PUT"])
@login_required
@role_required("admin")
def api_save_settings():
    """Upsert studio settings into the database."""
    data = request.get_json() or {}
    data["key"] = "studio"
    data["updated_at"] = datetime.now()
    mongo.db.settings.update_one(
        {"key": "studio"},
        {"$set": data},
        upsert=True
    )
    return jsonify({"success": True, "message": "Pengaturan berhasil disimpan"})
