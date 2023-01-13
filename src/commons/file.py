import os
from src.models.comments_model import Comments
from bson import ObjectId
import json
class File(json.JSONEncoder):
    def upload(self, file_location,file):
        with open(file_location, "wb+") as file_object:
            file_object.write(file.read())
        file_object.close()
        return {"code":200}

    def delete(self,file_name):
        if os.path.exists('file/' + file_name):
            os.remove('file/' + file_name)
        return {"code":200}