from flask import Blueprint, render_template, request, flash, redirect, url_for
from backend.app.services.resource_service import ResourceService
from backend.app.services.booking_service import BookingService

public_bp = Blueprint('public', __name__)
resource_service = ResourceService()
booking_service = BookingService()

@public_bp.route("/")
def index():
    artists = resource_service.get_artists(limit=3)
    services = resource_service.get_services(limit=3)
    gallery = resource_service.get_gallery(limit=4)
    return render_template("index.html", artists=artists, services=services, gallery=gallery)

@public_bp.route("/artists")
def artists_page():
    artists = resource_service.get_artists()
    return render_template("artists.html", artists=artists)

@public_bp.route("/services")
def services_page():
    services = resource_service.get_services()
    return render_template("services.html", services=services)

@public_bp.route("/gallery")
def gallery_page():
    gallery = resource_service.get_gallery()
    return render_template("gallery.html", gallery=gallery)
