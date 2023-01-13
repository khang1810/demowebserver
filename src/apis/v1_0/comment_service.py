from flask import Blueprint,request
from src.controllers.comments_controller import Comment
from src.commons.token_required import token_required
from src.commons.check_user import check_user
from src.models.comments_model import Comments
from bson import ObjectId
comments = Blueprint('comments', __name__)

@comments.route('/',methods=['GET'])
def dashboard():
    return "DASHBOARD"

@comments.route('/list_comt',methods=['GET'])
@token_required
def get_list_comments(current_user):
    return Comment.get_list_comments()

"""
@api {get} /api/v1.0/?last_id=<last_id>&post_id=<post_id> Get List Comments
@apiName GetListComments
@apiGroup Comments
@apiHeader {String} Authorization giá trị token(hết hạn sau 60p) VD:Bearer {token}.
@apiParam {String} post_id id của bài viết cần lấy comment
@apiParam {String} [parent=None] id của comment cha
@apiParam {String} [last_id=None] id của comment đứng trước 20 comment cần lấy
@apiSuccessExample {json} Success-Response:
{
    "code": 200,
    "data": [
        {
            "_id": {
                "$oid": "63438213cb89d1fdd24f14c9"
            },
            "content": "comment 3",
            "created_time": 1665368595.92787,
            "files_id": [],
            "parent": null,
            "path": [],
            "post_id": "633e976e989e16a60098f725",
            "update_time": 1665368595.92787,
            "updated_by": "632ffa9653ce43fdcd0984ef",
            "user_id": "632ffa9653ce43fdcd0984ef"
        },
        {
            "_id": {
                "$oid": "63438211cb89d1fdd24f14c8"
            },
            "content": "comment 2",
            "created_time": 1665368593.17697,
            "files_id": [],
            "parent": null,
            "path": [],
            "post_id": "633e976e989e16a60098f725",
            "update_time": 1665368593.17697,
            "updated_by": "632ffa9653ce43fdcd0984ef",
            "user_id": "632ffa9653ce43fdcd0984ef"
        },
        {
            "_id": {
                "$oid": "6343820dcb89d1fdd24f14c7"
            },
            "content": "comment 1",
            "created_time": 1665368589.876072,
            "files_id": [],
            "parent": null,
            "path": [],
            "post_id": "633e976e989e16a60098f725",
            "update_time": 1665368589.876072,
            "updated_by": "632ffa9653ce43fdcd0984ef",
            "user_id": "632ffa9653ce43fdcd0984ef"
        }
    ],
    "last_id":"6343820dcb89d1fdd24f14c7"
}
"""

@comments.route('/add_comment',methods=['POST'])
@token_required
def add_comment(current_user):
    post_id=request.form.get('post_id')
    return Comment.add_comment(comment_id=None,current_user=current_user,post_id=post_id)

"""
@api {post} /api/v1.0/add_comment add comments
@apiName addComments
@apiGroup Comments
@apiHeader {String} Authorization giá trị token(hết hạn sau 60p) VD:Bearer {token}.
@apiBody {String}   post_id   id của post có comment này.
@apiBody {String}   content   content comment này.
@apiSuccessExample {json} Success-Response:
{
    "code": 200,
    "data": {
        "comment_id": "63477d84b866da75dd5b5d97",
        "content": "bb",
        "created_time": 1665629572.786058,
        "files_id": [],
        "parent": null,
        "path": [],
        "post_id": "633e976e989e16a60098f725",
        "update_time": 1665629572.786058,
        "updated_by": "632ffa9653ce43fdcd0984ef",
        "user_id": "632ffa9653ce43fdcd0984ef"
    }
}
"""

@comments.route('/reply',methods=['POST'])
@token_required
def reply(current_user):
    comments_model=Comments()
    comment_id=request.form.get('comment_id')
    detail_parent=comments_model.get_comment_details({"_id":ObjectId(comment_id)})
    if detail_parent==None:
        return {'code':0,'msg':'comment khong ton tai'}
    post_id=detail_parent.get('post_id')
    return Comment.add_comment(comment_id=comment_id,current_user=current_user,post_id=post_id)

"""
@api {post} /api/v1.0/reply reply comments
@apiName repComments
@apiGroup Comments
@apiHeader {String} Authorization giá trị token(hết hạn sau 60p) VD:Bearer {token}.
@apiBody {String}   comment_id   id của comment mà comment này reply.
@apiBody {String}   content   content comment này.
@apiSuccessExample {json} Success-Response:
{
    "code": 200,
    "data": {
        "comment_id": "63477d84b866da75dd5b5d97",
        "content": "bb",
        "created_time": 1665629572.786058,
        "files_id": [],
        "parent": 634380ba0c674e366e3bbf14,
        "path": [],
        "post_id": "633e976e989e16a60098f725",
        "update_time": 1665629572.786058,
        "updated_by": "632ffa9653ce43fdcd0984ef",
        "user_id": "632ffa9653ce43fdcd0984ef"
    }
}
"""

@comments.route('/reactions',methods=['POST'])
@token_required
def reactions(current_user):
    comment_id=request.form.get('comment_id')
    type=request.form.get('type')
    return Comment.reaction(comment_id=comment_id,current_user=current_user,type=type)

"""
@api {post} /api/v1.0/reactions reaction comments
@apiName reactComments
@apiGroup Comments
@apiHeader {String} Authorization giá trị token(hết hạn sau 60p) VD:Bearer {token}.
@apiBody {String}   type   loại react.
@apiBody {String}   comment_id   comment được react.
@apiSuccessExample {json} Success-Response:
{
    "code": 200,
    "data": {
        "comment_id": "634380ba0c674e366e3bbf14",
        "type": "like",
        "user_id": "632ffa9653ce43fdcd0984ef"
    }
}
"""

@comments.route('/edit',methods=['POST'])
@token_required
def edit(current_user):
    comment_id=request.form.get('comment_id')
    if check_user(comment_id,current_user)==False:
        return {'code':0}
    return Comment.edit(comment_id=comment_id,current_user=current_user)

"""
@api {post} /api/v1.0/edit edit comments content
@apiName editComments
@apiGroup Comments
@apiHeader {String} Authorization giá trị token(hết hạn sau 60p) VD:Bearer {token}.
@apiBody {String}   content   nội dung sau khi sửa.
@apiBody {String}   comment_id   id comment cần sửa.
@apiSuccessExample {json} Success-Response:
{
    "code": 200,
    "msg": "633e9c5ca0ba76c085d4a68c edited"
}
"""

@comments.route('/delete',methods=['POST'])
@token_required
def delete(current_user):
    comment_id=request.form.get('comment_id')
    if check_user(comment_id,current_user)==False:
        return {'code':0}
    return Comment.delete(comment_id=comment_id,current_user=current_user)

"""
@api {post} /api/v1.0/delete delete comments
@apiName deleteComments
@apiGroup Comments
@apiHeader {String} Authorization giá trị token(hết hạn sau 60p) VD:Bearer {token}.
@apiBody {String}   comment_id   id comment cần xóa.
@apiSuccessExample {json} Success-Response:
{
    "code": 200,
    "deleted": "633e9c5ca0ba76c085d4a68c"
}
"""

@comments.route('/upload_file',methods=['POST'])
@token_required
def upload_file(current_user):
    comment_id=request.form.get('comment_id')
    return Comment.upload_file(current_user=current_user,comment_id=comment_id)

"""
@api {post} /api/v1.0/upload_file upload file
@apiName uploadfile
@apiGroup Comments
@apiHeader {String} Authorization giá trị token(hết hạn sau 60p) VD:Bearer {token}.
@apiBody {String}   comment_id   id comment có file đính kèm.
@apiBody {File}   attach_files   các file đính kèm.
@apiSuccessExample {json} Success-Response:
{
    "code": 200,
    "data": {
        "file_name": "efffe789-6fc9-4893-a33d-0aafad7678ac.jpg",
        "files_id": [
            "6347820a64bbd25268da00bf",
            "6347820a64bbd25268da00c0",
            "6347821e64bbd25268da00c1",
            "6347821e64bbd25268da00c2"
        ],
        "user_id": "632ffa9653ce43fdcd0984ef"
    }
}
"""

@comments.route('/delete_file',methods=['POST'])
@token_required
def delete_file(current_user):
    file_name=request.form.get('file_name')
    comment_id=request.form.get('comment_id')
    return Comment.delete_file(file_name=file_name,current_user=current_user,comment_id=comment_id)

"""
@api {post} /api/v1.0/delete_file delete file
@apiName deletefile
@apiGroup Comments
@apiHeader {String} Authorization giá trị token(hết hạn sau 60p) VD:Bearer {token}.
@apiBody {String}   file_name   tên file cần xóa.
@apiBody {String}   comment_id   id của comment đính kèm file.
@apiSuccessExample {json} Success-Response:
{
    "code": 200,
    "deleted": "50003e49-7753-470e-9bcb-e105ee194091.jpg"
}
"""