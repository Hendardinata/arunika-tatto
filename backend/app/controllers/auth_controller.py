from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from backend.app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user, message = auth_service.authenticate_user(email, password)
        if user:
            session["user_id"] = str(user["_id"])
            session["fullname"] = user["fullname"]
            session["role"] = user.get("role", "customer")
            flash(message, "success")
            
            if session["role"] == "admin":
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('public.index'))
            
        flash(message, "error")
        return redirect(url_for('auth.login'))
        
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        
        success, message = auth_service.register_user(fullname, email, password)
        if success:
            flash(message, "success")
            return redirect(url_for('auth.login'))
        else:
            flash(message, "error")
            
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Anda telah logout.", "info")
    return redirect(url_for('public.index'))
