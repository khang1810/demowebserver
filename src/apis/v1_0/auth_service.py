from flask import Blueprint
from src.controllers.auth_controller import Authenticate
auth1 = Blueprint('auth', __name__)
@auth1.route('/login',methods=['POST'])
def login():
    return Authenticate.login()

"""
@api {post} /login get token 
@apiName Get token
@apiGroup Auth
@apiBody {String}   username   tài khoản.
@apiBody {String}   password   mật khẩu.
@apiSuccessExample {json} Success-Response:
{
    "token": "{token}"
}
"""