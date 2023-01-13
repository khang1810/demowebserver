try:
    from models import BaseModel
except:
    from src.models import BaseModel
class POST(BaseModel):
    collection_name = "post"
    def get_post_detail(self,search_option=None,field_select=None):
        try:
            return self.find_one(search_option,field_select)
        except Exception as ex:
            print(ex)
            return None