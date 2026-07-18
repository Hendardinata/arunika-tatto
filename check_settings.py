import sys
import os
sys.path.append(os.path.abspath('.'))

from run_server import app
from backend.app.database.connection import mongo

with app.app_context():
    doc = mongo.db.settings.find_one({"key": "studio"})
    print("SETTINGS IN DB:", doc)
