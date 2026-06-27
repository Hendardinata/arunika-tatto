from flask import Blueprint, render_template
from backend.app.middlewares.auth_middleware import login_required, role_required

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
@login_required
@role_required("admin", "superadmin")
def dashboard():
    return render_template("admin/dashboard.html")

@admin_bp.route("/setup-admin")
def setup_admin():
    from backend.app.services.auth_service import AuthService
    from backend.app.repositories.domain_repositories import UserRepository
    from werkzeug.security import generate_password_hash
    from datetime import datetime
    
    user_repo = UserRepository()
    existing_admin = user_repo.find_one({"email": "admin@inkmaster.com"})
    if existing_admin:
        return "Admin account already exists: admin@inkmaster.com / admin123"
        
    hashed_pwd = generate_password_hash("admin123")
    new_admin = {
        "fullname": "Administrator",
        "email": "admin@inkmaster.com",
        "password": hashed_pwd,
        "role": "admin",
        "created_at": datetime.now()
    }
    user_repo.insert(new_admin)
    return "Admin account created successfully: admin@inkmaster.com / admin123"
