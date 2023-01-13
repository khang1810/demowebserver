try:
    from models import BaseModel
except:
    from src.models import BaseModel
class Commentslog(BaseModel):
    collection_name = "comments_log"
    def get_comment_log(self,search_option=None,field_select=None):
        try:
            return self.find_one(search_option,field_select)
        except Exception as ex:
            return None
            
    def save_comment_log(self,dict):
        try:
            return self.insert(dict)
        except Exception as ex:
            return None