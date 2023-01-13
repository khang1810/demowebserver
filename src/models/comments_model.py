try:
    from models import BaseModel
except:
    from src.models import BaseModel
class Comments(BaseModel):
    collection_name = "comments"
    def get_all_comments(self,search_option=None,field_select=None):
        try:
            return self.find(search_option,field_select)
        except Exception as ex:
            return None
            
    def append_topic_comments(self,dict):
        try:
            return self.insert(dict)
        except Exception as ex:
            return None

    def update_comment(self,query,value):
        try:
            return self.update(query,value)
        except Exception as ex:
            return None

    def get_comment_details(self,search_option=None,field_select=None):
        try:
            return self.find_one(search_option,field_select)
        except Exception as ex:
            print(ex)
            return None
            
    def delete_comment(self,dict):
        try:
            return self.delete_many(dict)
        except Exception as ex:
            return None