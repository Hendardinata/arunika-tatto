from bson import ObjectId

class BaseRepository:
    def __init__(self, collection):
        self.collection = collection

    def find_all(self, query=None, limit=0):
        query = query or {}
        return list(self.collection.find(query).limit(limit))

    def find_by_id(self, document_id):
        try:
            return self.collection.find_one({"_id": ObjectId(document_id)})
        except:
            return None

    def find_one(self, query):
        return self.collection.find_one(query)

    def insert(self, data):
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def update(self, document_id, data):
        try:
            self.collection.update_one(
                {"_id": ObjectId(document_id)},
                {"$set": data}
            )
            return True
        except:
            return False

    def delete(self, document_id):
        try:
            self.collection.delete_one({"_id": ObjectId(document_id)})
            return True
        except:
            return False

    def count(self, query=None):
        query = query or {}
        return self.collection.count_documents(query)
