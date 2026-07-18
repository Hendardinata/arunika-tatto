import sys
import os
sys.path.append(os.path.abspath('.'))

from run_server import app
from backend.app.database.connection import mongo
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

with app.app_context():
    doc = mongo.db.settings.find_one({"key": "studio"})
    with open('settings_dump.json', 'w') as f:
        json.dump(doc or {}, f, cls=JSONEncoder)
