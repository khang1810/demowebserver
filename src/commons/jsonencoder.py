import json
from bson import ObjectId
from bson import json_util

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

    def parse_json(self,data):
        return json.loads(json_util.dumps(data))