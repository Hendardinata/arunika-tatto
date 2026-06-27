from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from backend.app.middlewares.auth_middleware import login_required, role_required
from backend.app.services.booking_service import BookingService
from backend.app.services.resource_service import ResourceService

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
