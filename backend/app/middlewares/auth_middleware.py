from functools import wraps
from flask import session, redirect, url_for, flash, request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash("Anda harus login terlebih dahulu.", "error")
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('user_id'):
                flash("Anda harus login terlebih dahulu.", "error")
                return redirect(url_for('auth.login', next=request.url))
            if session.get('role') not in roles:
                flash("Anda tidak memiliki akses ke halaman ini.", "error")
                return redirect(url_for('public.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
