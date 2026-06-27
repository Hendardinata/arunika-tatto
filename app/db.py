from pymongo import MongoClient
from bson.objectid import ObjectId

class PyMongoShim:
    def __init__(self):
        self.db = None
        self.client = None

    def init_app(self, app):
        uri = app.config.get("MONGO_URI", "mongodb://localhost:27017/tattoo_studio")
        self.client = MongoClient(uri)
        # Parse DB name from URI or fallback
        db_name = uri.split("/")[-1].split("?")[0]
        if not db_name:
            db_name = "tattoo_studio"
        self.db = self.client[db_name]

mongo = PyMongoShim()

def serialize_doc(doc):
    """Helper to convert MongoDB types to JSON serializable formats."""
    if not doc:
        return None
        
    for key, value in doc.items():
        # Handle ObjectId
        if hasattr(value, "is_valid") and hasattr(value, "generation_time"): # weak check for ObjectId
            doc[key] = str(value)
        # Handle datetime
        elif hasattr(value, "isoformat"):
            doc[key] = value.isoformat()
            
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

def serialize_list(cursor):
    """Helper to convert a cursor to a list of serialized dicts."""
    return [serialize_doc(doc) for doc in cursor]
