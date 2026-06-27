from pymongo import MongoClient

class PyMongoShim:
    """A minimal wrapper around raw PyMongo to mimic flask_pymongo"""
    def __init__(self, app=None):
        self.cx = None
        self.db = None
        if app is not None:
            self.init_app(app)
            
    def init_app(self, app):
        uri = app.config.get("MONGO_URI", "mongodb://localhost:27017/inkmaster")
        self.cx = MongoClient(uri)
        db_name = uri.split("/")[-1].split("?")[0]
        if not db_name:
            db_name = "inkmaster"
        self.db = self.cx[db_name]

mongo = PyMongoShim()
