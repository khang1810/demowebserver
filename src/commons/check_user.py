from src.models.users_model import Users
from src.models.comments_model import Comments
from bson import ObjectId

def check_user(comment_id,current_user):
    users_model=Users()
    comments_model=Comments()
    comment_detail=comments_model.get_comment_details({"_id":ObjectId(comment_id)})
    if comment_detail == None:
        return {'code':0,'msg':'comment khong ton tai'}
    author_id=comment_detail.get('user_id')
    current_id=str(current_user.get('_id'))
    user = users_model.get_user({"_id":ObjectId(current_id)})
    user_type=user.get('type')
    if user_type!='admin' and current_id!=author_id:
        return False
    return True


        

