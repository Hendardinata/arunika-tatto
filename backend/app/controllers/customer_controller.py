from flask import Blueprint, render_template, request, flash, redirect, url_for, session, current_app
from backend.app.middlewares.auth_middleware import login_required, role_required
from backend.app.services.booking_service import BookingService
from backend.app.services.resource_service import ResourceService
import os
from werkzeug.utils import secure_filename
from datetime import datetime

customer_bp = Blueprint('customer', __name__)
booking_service = BookingService()
resource_service = ResourceService()

@customer_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("customer/dashboard.html")

@customer_bp.route("/booking", methods=["GET", "POST"])
@login_required
def booking_page():
    if request.method == "POST":
        artist_id = request.form.get("artist_id")
        service_id = request.form.get("service_id")
        date = request.form.get("date")
        time = request.form.get("time")
        notes = request.form.get("notes", "")
        
        user_id = session.get("user_id")
        
        # Note: reference_image not yet stored in DB model by default, but we should safely handle the upload if needed in the future
        file = request.files.get("reference_image")
        if file and file.filename:
            upload_folder = current_app.config.get("UPLOAD_FOLDER", "frontend/static/uploads")
            os.makedirs(upload_folder, exist_ok=True)
            filename = f"ref_{int(datetime.now().timestamp())}_{secure_filename(file.filename)}"
            file.save(os.path.join(upload_folder, filename))
            notes += f"\n[Reference Image: {filename}]"
        
        success, msg = booking_service.create_booking(user_id, artist_id, service_id, date, time, notes)
        
        if success:
            flash(msg, "success")
            return redirect(url_for('customer.dashboard'))
        else:
            flash(msg, "error")
            return redirect(url_for('customer.booking_page'))
            
    artists = resource_service.get_artists()
    services = resource_service.get_services()
    return render_template("booking.html", artists=artists, services=services)


@customer_bp.route("/payment", methods=["GET", "POST"])
@login_required
def payment_page():
    if request.method == "POST":
        booking_id = request.form.get("booking_id")
        file = request.files.get("payment_proof")
        
        if not booking_id or not file or not file.filename:
            flash("Data atau bukti pembayaran tidak lengkap", "error")
            return redirect(url_for('customer.dashboard'))
            
        upload_folder = current_app.config.get("UPLOAD_FOLDER", "frontend/static/uploads")
        os.makedirs(upload_folder, exist_ok=True)
        filename = f"pay_{int(datetime.now().timestamp())}_{secure_filename(file.filename)}"
        file.save(os.path.join(upload_folder, filename))
        
        success, msg = booking_service.upload_payment_proof(booking_id, filename)
        if success:
            flash(msg, "success")
        else:
            flash(msg, "error")
            
        return redirect(url_for('customer.dashboard'))

    # GET request
    booking_id = request.args.get("booking")
    if not booking_id:
        flash("ID Booking tidak valid", "error")
        return redirect(url_for('customer.dashboard'))
        
    booking = booking_service.booking_repo.find_by_id(booking_id)
    if not booking:
        flash("Booking tidak ditemukan", "error")
        return redirect(url_for('customer.dashboard'))
        
    return render_template("payment/index.html", booking=booking)
