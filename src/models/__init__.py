from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db_name = 'testdb'

class BaseModel:
    collection_name = ''
    def _db(self):
        return client[db_name]

    def get_db(self):
        return client[db_name]

    def insert(self, dictionary):
        db = client[db_name]
        return db[self.collection_name].insert_one(dictionary)

    def find_one(self, search_option=None, field_select=None):
        db = client[db_name]
        return db[self.collection_name].find_one(search_option, field_select)

    def distinct(self, fields, query):
        db = client[db_name]

        if type(fields) is str:
            return db[self.collection_name].distinct(fields, query)

        return None

    def find(self, search_option=None, field_select=None):
        db = client[db_name]
        if field_select:
            return db[self.collection_name].find(search_option, field_select)
        return db[self.collection_name].find(search_option)

    def update(self, search_option, field_select):
        db = client[db_name]
        if field_select:
            return db[self.collection_name].update_one(search_option, field_select)
        return db[self.collection_name].update_one(search_option)

    def delete(self, dictionary):
        db = client[db_name]
        return db[self.collection_name].delete_one(dictionary)

    def delete_many(self, dictionary):
        db = client[db_name]
        return db[self.collection_name].delete_many(dictionary)

    def count(self, dictionary):
        db = client[db_name]
        return db[self.collection_name].count_documents(dictionary)