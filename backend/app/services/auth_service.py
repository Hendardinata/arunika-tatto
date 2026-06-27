from werkzeug.security import generate_password_hash, check_password_hash
from backend.app.repositories.domain_repositories import UserRepository
from datetime import datetime

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, fullname, email, password):
        existing_user = self.user_repo.find_one({"email": email})
        if existing_user:
            return False, "Email sudah terdaftar!"

        hashed_pwd = generate_password_hash(password)
        new_user = {
            "fullname": fullname,
            "email": email,
            "password": hashed_pwd,
            "role": "customer",
            "created_at": datetime.now()
        }
        self.user_repo.insert(new_user)
        return True, "Registrasi berhasil! Silakan login."

    def authenticate_user(self, email, password):
        user = self.user_repo.find_one({"email": email})
        if not user or not check_password_hash(user["password"], password):
            return None, "Email atau password salah!"
        return user, "Login berhasil!"
