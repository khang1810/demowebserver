from flask import request,session,make_response,jsonify
import traceback,json
from main import app
from src.models.users_model import Users
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
class Authenticate:
    def login():
        users_model=Users()
        user_name = request.form.get('username')
        password = request.form.get('password')
        if not user_name or not password:
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
            )
    
        user = users_model.get_user({"user_name":user_name})
    
        if not user:
            # returns 401 if user does not exist
            return make_response(
                'Could not verify',
                401,
                {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
            )
    
        if check_password_hash(generate_password_hash(password), password):
            # generates the JWT Token
            token = jwt.encode({
                'public_id': user.get('public_id'),
                'exp' : datetime.utcnow() + timedelta(minutes = 60)
            }, app.config['SECRET_KEY'])
    
            return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
        # returns 403 if password is wrong
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
        )