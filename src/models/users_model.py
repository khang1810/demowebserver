try:
    from models import BaseModel
except:
    from src.models import BaseModel
class Users(BaseModel):
    collection_name = "users"
    def get_user(self,search_option=None,field_select=None):
        try:
            return self.find_one(search_option,field_select)
        except Exception as ex:
            return None