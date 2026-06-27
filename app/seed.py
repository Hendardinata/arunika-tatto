from flask import Flask
from config import Config
from db import mongo
from datetime import datetime
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)
mongo.init_app(app)

DUMMY_ARTISTS = [
    {"name": "Kevin Hartono", "instagram": "kevin_tattoo",
     "specialization": "Realism", "experience": "8 tahun", "status": "active",
     "description": "Spesialis portrait realism dan black & grey."},
    {"name": "Rina Wijaya", "instagram": "rina_ink",
     "specialization": "Watercolor", "experience": "5 tahun", "status": "active",
     "description": "Menguasai watercolor dan floral tattoo."},
    {"name": "Bobby Pratama", "instagram": "bobby_tribal",
     "specialization": "Tribal & Traditional", "experience": "10 tahun", "status": "active",
     "description": "Ahli tribal tradisional dan neo-traditional."},
    {"name": "Sari Dewi", "instagram": "sari_geometric",
     "specialization": "Geometric", "experience": "6 tahun", "status": "active",
     "description": "Spesialis geometric dan dotwork."},
]

DUMMY_SERVICES = [
    {"name": "Small Tattoo", "price": 500000, "duration": 60,
     "description": "Tattoo ukuran kecil (3-5 cm). Cocok untuk desain minimalis."},
    {"name": "Medium Tattoo", "price": 1200000, "duration": 120,
     "description": "Tattoo ukuran sedang (5-10 cm) dengan detail."},
    {"name": "Large Tattoo", "price": 2500000, "duration": 240,
     "description": "Tattoo ukuran besar dengan full shading."},
    {"name": "Cover Up", "price": 3000000, "duration": 300,
     "description": "Menutup tattoo lama dengan desain baru."},
    {"name": "Custom Design", "price": 350000, "duration": 0,
     "description": "Konsultasi dan pembuatan desain custom."},
]

DUMMY_GALLERY = [
    {"title": "Dragon Sleeve", "artist_name": "Kevin Hartono",
     "category": "realism", "image": None},
    {"title": "Floral Shoulder", "artist_name": "Rina Wijaya",
     "category": "watercolor", "image": None},
    {"title": "Mandala Back", "artist_name": "Bobby Pratama",
     "category": "tribal", "image": None},
]

def seed_db():
    with app.app_context():
        # Clear existing
        mongo.db.artists.delete_many({})
        mongo.db.services.delete_many({})
        mongo.db.gallery.delete_many({})
        mongo.db.users.delete_many({})

        # Insert Dummies
        mongo.db.artists.insert_many(DUMMY_ARTISTS)
        mongo.db.services.insert_many(DUMMY_SERVICES)
        mongo.db.gallery.insert_many(DUMMY_GALLERY)

        # Create an admin user
        mongo.db.users.insert_one({
            "fullname": "Admin Tattoo",
            "email": "admin@inkmaster.com",
            "password": generate_password_hash("admin123"),
            "role": "admin",
            "created_at": datetime.now()
        })
        
        # Create a customer user
        mongo.db.users.insert_one({
            "fullname": "Andi Pratama",
            "email": "andi@email.com",
            "password": generate_password_hash("andi123"),
            "role": "customer",
            "phone": "628123456789",
            "created_at": datetime.now()
        })
        print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_db()
