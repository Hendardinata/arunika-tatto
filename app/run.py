"""
InkMaster Studio - Tattoo Studio Management System
Backend Integrated with MongoDB
"""
import os
import secrets
from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (Flask, render_template, request, jsonify,
                   redirect, url_for, session, flash, send_from_directory)
from config import Config
from db import mongo, serialize_list, serialize_doc

# ---------------------------------------------------------------------------
# App Factory
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)

# Initialize PyMongo
mongo.init_app(app)

# ---------------------------------------------------------------------------
# Pages (Server-side rendered)
# ---------------------------------------------------------------------------
@app.route("/setup-admin")
def setup_admin():
    admin = mongo.db.users.find_one({"email": "admin@inkmaster.com"})
    if admin:
        return "Admin sudah ada! Silakan login dengan Email: <b>admin@inkmaster.com</b> | Password: <b>admin123</b> <br><br> <a href='/login'>Ke Halaman Login</a>"
    
    mongo.db.users.insert_one({
        "fullname": "Super Admin",
        "email": "admin@inkmaster.com",
        "password": generate_password_hash("admin123"),
        "role": "admin",
        "created_at": datetime.now()
    })
    return "Data Admin berhasil dibuat! Silakan login dengan Email: <b>admin@inkmaster.com</b> | Password: <b>admin123</b> <br><br> <a href='/login'>Ke Halaman Login</a>"

@app.route("/")
def index():
    artists = serialize_list(mongo.db.artists.find().limit(3))
    services = serialize_list(mongo.db.services.find().limit(3))
    gallery = serialize_list(mongo.db.gallery.find().limit(3))
    return render_template("index.html", artists=artists, services=services, gallery=gallery)

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/artists")
def artists_page():
    artists = serialize_list(mongo.db.artists.find())
    return render_template("artists.html", artists=artists)

@app.route("/services")
def services_page():
    services = serialize_list(mongo.db.services.find())
    return render_template("services.html", services=services)

@app.route("/gallery")
def gallery_page():
    gallery = serialize_list(mongo.db.gallery.find())
    return render_template("gallery.html", gallery=gallery)

@app.route("/booking", methods=["GET", "POST"])
def booking_page():
    if "user_id" not in session:
        flash("Silakan login untuk melakukan booking.", "info")
        return redirect(url_for("login_page"))
        
    if request.method == "POST":
        artist_id = request.form.get("artist_id")
        service_id = request.form.get("service_id")
        date = request.form.get("date")
        time = request.form.get("time")
        notes = request.form.get("notes", "")
        
        user_id = session.get("user_id")
        
        try:
            artist = mongo.db.artists.find_one({"_id": ObjectId(artist_id)}) if artist_id else None
            service = mongo.db.services.find_one({"_id": ObjectId(service_id)}) if service_id else None
            user = mongo.db.users.find_one({"_id": ObjectId(user_id)}) if user_id else None
        except:
            artist = service = user = None
            
        if not artist or not service or not user:
            flash("Data artist atau service tidak valid", "error")
            return redirect(url_for("booking_page"))
            
        code = f"INV-{datetime.now().strftime('%Y%m%d%H%M')}"
        
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
        
        # Handle file upload if any
        ref_image = request.files.get("reference_image")
        if ref_image and ref_image.filename:
            filename = f"ref_{code}_{ref_image.filename}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            ref_image.save(file_path)
            new_booking["reference_image"] = filename
            
        mongo.db.bookings.insert_one(new_booking)
        flash("Booking berhasil! Menunggu konfirmasi admin.", "success")
        return redirect(url_for("customer_dashboard"))
        
    artists = serialize_list(mongo.db.artists.find({"status": "active"}))
    services = serialize_list(mongo.db.services.find())
    return render_template("booking.html", artists=artists, services=services)

@app.route("/dashboard")
def customer_dashboard():
    if session.get("role") != "customer":
        return redirect(url_for("login_page"))
    return render_template("customer/dashboard.html")

@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect(url_for("login_page"))
    return render_template("admin/dashboard.html")

@app.route("/payment")
def payment_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("payment/index.html")

# ---------------------------------------------------------------------------
# Auth endpoints
# ---------------------------------------------------------------------------
@app.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    
    user = mongo.db.users.find_one({"email": email})
    if user and check_password_hash(user.get("password", ""), password):
        session["user_id"] = str(user["_id"])
        session["fullname"] = user.get("fullname", "")
        session["email"] = email
        session["role"] = user.get("role", "customer")
        flash("Login berhasil!", "success")
        if session["role"] == "admin":
            return redirect(url_for("admin_dashboard"))
        return redirect(url_for("customer_dashboard"))
        
    flash("Email atau password salah!", "error")
    return redirect(url_for("login_page"))

@app.route("/register", methods=["POST"])
def register_post():
    fullname = request.form.get("fullname", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    
    if not (fullname and email and password):
        flash("Lengkapi semua field!", "error")
        return redirect(url_for("register_page"))
        
    existing = mongo.db.users.find_one({"email": email})
    if existing:
        flash("Email sudah terdaftar!", "error")
        return redirect(url_for("register_page"))
        
    hashed_pw = generate_password_hash(password)
    new_user = {
        "fullname": fullname,
        "email": email,
        "password": hashed_pw,
        "role": "customer",
        "created_at": datetime.now()
    }
    res = mongo.db.users.insert_one(new_user)
    
    session["user_id"] = str(res.inserted_id)
    session["fullname"] = fullname
    session["email"] = email
    session["role"] = "customer"
    flash("Registrasi berhasil!", "success")
    return redirect(url_for("customer_dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for("index"))

# ---------------------------------------------------------------------------
# API Endpoints (JSON)
# ---------------------------------------------------------------------------
@app.route("/api/artists")
def api_artists():
    artists = serialize_list(mongo.db.artists.find())
    return jsonify({"success": True, "artists": artists})

@app.route("/api/artists", methods=["POST"])
def api_add_artist():
    data = request.get_json()
    new_artist = {
        "name": data.get("name", ""),
        "instagram": data.get("instagram", ""),
        "specialization": data.get("specialization", ""),
        "experience": data.get("experience", ""),
        "description": data.get("description", ""),
        "status": "active",
    }
    res = mongo.db.artists.insert_one(new_artist)
    new_artist["_id"] = str(res.inserted_id)
    return jsonify({"success": True, "artist": new_artist})

@app.route("/api/services")
def api_services():
    services = serialize_list(mongo.db.services.find())
    return jsonify({"success": True, "services": services})

@app.route("/api/services", methods=["POST"])
def api_add_service():
    data = request.get_json()
    new_service = {
        "name": data.get("name", ""),
        "price": int(data.get("price", 0)),
        "duration": int(data.get("duration", 60)),
        "description": data.get("description", ""),
    }
    res = mongo.db.services.insert_one(new_service)
    new_service["_id"] = str(res.inserted_id)
    return jsonify({"success": True, "service": new_service})

@app.route("/api/services/<service_id>", methods=["DELETE"])
def api_delete_service(service_id):
    try:
        mongo.db.services.delete_one({"_id": ObjectId(service_id)})
        return jsonify({"success": True})
    except:
        return jsonify({"success": False, "message": "Invalid ID"}), 400

@app.route("/api/gallery")
def api_gallery():
    gallery = serialize_list(mongo.db.gallery.find())
    return jsonify({"success": True, "gallery": gallery})

@app.route("/api/gallery", methods=["POST"])
def api_add_gallery():
    title = request.form.get("title", "")
    category = request.form.get("category", "other")
    new_item = {
        "title": title,
        "artist_name": "Admin", # Should ideally map to a real artist id
        "category": category,
        "image": None,
    }
    res = mongo.db.gallery.insert_one(new_item)
    new_item["_id"] = str(res.inserted_id)
    return jsonify({"success": True, "gallery": new_item})

@app.route("/api/bookings")
def api_bookings():
    status_filter = request.args.get("status")
    query = {}
    if status_filter:
        query["status"] = status_filter
    bookings = serialize_list(mongo.db.bookings.find(query).sort("created_at", -1))
    return jsonify({"success": True, "bookings": bookings})

@app.route("/api/bookings/<booking_id>")
def api_booking_detail(booking_id):
    try:
        booking = serialize_doc(mongo.db.bookings.find_one({"_id": ObjectId(booking_id)}))
        if not booking:
            return jsonify({"success": False, "message": "Booking not found"}), 404
        return jsonify({"success": True, "booking": booking})
    except:
        return jsonify({"success": False, "message": "Invalid ID"}), 400

@app.route("/api/bookings/<booking_id>", methods=["PUT"])
def api_update_booking(booking_id):
    data = request.get_json()
    status = data.get("status")
    if not status:
        return jsonify({"success": False, "message": "Missing status"}), 400
        
    try:
        result = mongo.db.bookings.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": {"status": status}}
        )
        if result.matched_count == 0:
            return jsonify({"success": False, "message": "Booking not found"}), 404
            
        booking = serialize_doc(mongo.db.bookings.find_one({"_id": ObjectId(booking_id)}))
        return jsonify({"success": True, "booking": booking})
    except:
        return jsonify({"success": False, "message": "Invalid ID"}), 400

@app.route("/api/slots")
def api_slots():
    date = request.args.get("date")
    artist_id = request.args.get("artist_id")
    
    if not date or not artist_id:
        return jsonify({"success": False, "slots": []})
        
    # All possible slots
    all_slots = ["08:00", "10:00", "13:00", "15:00", "17:00"]
    
    # Find booked slots for this date and artist
    bookings = mongo.db.bookings.find({
        "date": date,
        "artist_id": artist_id,
        "status": {"$nin": ["cancelled"]}
    })
    
    booked_times = [b.get("time") for b in bookings]
    available_slots = [s for s in all_slots if s not in booked_times]
    
    return jsonify({"success": True, "slots": available_slots})

@app.route("/api/my-bookings")
def api_my_bookings():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "message": "Not logged in"}), 401
    
    bookings = serialize_list(mongo.db.bookings.find({"customer_id": user_id}).sort("created_at", -1))
    return jsonify({"success": True, "bookings": bookings})

@app.route("/api/payments")
def api_payments():
    payments = serialize_list(mongo.db.payments.find().sort("created_at", -1))
    return jsonify({"success": True, "payments": payments})

@app.route("/api/payments/<payment_id>/confirm", methods=["POST"])
def api_confirm_payment(payment_id):
    try:
        payment = mongo.db.payments.find_one({"_id": ObjectId(payment_id)})
        if not payment:
            return jsonify({"success": False, "message": "Payment not found"}), 404
            
        mongo.db.payments.update_one(
            {"_id": ObjectId(payment_id)},
            {"$set": {"payment_status": "confirmed", "confirmed_at": datetime.now()}}
        )
        
        mongo.db.bookings.update_one(
            {"_id": ObjectId(payment.get("booking_id"))},
            {"$set": {"status": "confirmed"}}
        )
        
        return jsonify({"success": True})
    except:
        return jsonify({"success": False, "message": "Invalid ID"}), 400

@app.route("/api/customers")
def api_customers():
    customers = serialize_list(mongo.db.users.find({"role": "customer"}))
    return jsonify({"success": True, "customers": customers})

@app.route("/api/payment/upload-proof", methods=["POST"])
def api_upload_proof():
    booking_id = request.form.get("booking_id")
    file = request.files.get("proof_image")
    
    if not booking_id or not file:
        return jsonify({"success": False, "message": "Missing data"}), 400
        
    try:
        booking = mongo.db.bookings.find_one({"_id": ObjectId(booking_id)})
        if not booking:
            return jsonify({"success": False, "message": "Booking not found"}), 404
            
        filename = f"proof_{booking_id}_{file.filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        mongo.db.bookings.update_one(
            {"_id": ObjectId(booking_id)},
            {"$set": {"status": "waiting_payment"}}
        )
        
        mongo.db.payments.insert_one({
            "booking_id": str(booking["_id"]),
            "booking_code": booking.get("booking_code"),
            "customer_name": booking.get("customer_name"),
            "amount": booking.get("service_price"),
            "payment_status": "uploaded",
            "proof_image": filename,
            "created_at": datetime.now()
        })
        
        return jsonify({"success": True, "message": "Bukti pembayaran berhasil diupload"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/api/dashboard/stats")
def api_dashboard_stats():
    # Helper to calculate stats
    total_bookings = mongo.db.bookings.count_documents({})
    waiting_payment = mongo.db.bookings.count_documents({"status": "waiting_payment"})
    completed = mongo.db.bookings.count_documents({"status": "completed"})
    
    pipeline = [
        {"$match": {"status": "completed"}},
        {"$group": {"_id": None, "total": {"$sum": "$service_price"}}}
    ]
    result = list(mongo.db.bookings.aggregate(pipeline))
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

# ---------------------------------------------------------------------------
# Static files & Uploads
# ---------------------------------------------------------------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ---------------------------------------------------------------------------
# Context processor — inject globals into templates
# ---------------------------------------------------------------------------
@app.context_processor
def inject_globals():
    return {
        "now": datetime.now(),
        "session": session,
    }

# ---------------------------------------------------------------------------
# JSON error handler for API routes
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "message": "Endpoint not found"}), 404
    return render_template("base.html"), 404

# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 InkMaster Studio Server running with MongoDB!")
    print("📍 http://127.0.0.1:5000")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)
