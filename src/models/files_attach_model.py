try:
    from models import BaseModel
except:
    from src.models import BaseModel
class FilesAttach(BaseModel):
    collection_name = "files"
    def get_files_details(self,search_option=None,field_select=None):
        try:
            return self.find_one(search_option,field_select)
        except Exception as ex:
            print(ex)
            return None

    def add_attach_files(self,dict):
        try:
            return self.insert(dict)
        except Exception as ex:
            return None

    def delete_attach_files_documents(self,dict):
        try:
            return self.delete(dict)
        except Exception as ex:
            return None

    def update_file(self,query,value):
        try:
            return self.update(query,value)
        except Exception as ex:
            return None

    def get_files_ids(self):
        try:
            return self.find({},{"_id":1})
        except Exception as ex:
            print(ex)
            return None

    def delete_many_attach_files_documents(self,dict):
        try:
            return self.delete_many(dict)
        except Exception as ex:
            return None