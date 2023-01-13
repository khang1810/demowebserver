try:
    from models import BaseModel
except:
    from src.models import BaseModel
class Reacts(BaseModel):
    collection_name = "reacts"
    def update_react(self,query,value):
        try:
            return self.update(query,value)
        except Exception as ex:
            return None

    def get_react_detail(self,search_option=None,field_select=None):
        try:
            return self.find_one(search_option,field_select)
        except Exception as ex:
            print(ex)
            return None

    def add_react_document(self,dict):
        try:
            return self.insert(dict)
        except Exception as ex:
            return None

    def delete_reacts_documents(self,dict):
        try:
            return self.delete(dict)
        except Exception as ex:
            return None

    def get_all_react_detail(self,search_option=None,field_select=None):
        try:
            return self.find(search_option,field_select)
        except Exception as ex:
            print(ex)
            return None

    def count_doc(self,search_option=None):
        try:
            return self.count(search_option)
        except Exception as ex:
            print(ex)
            return None