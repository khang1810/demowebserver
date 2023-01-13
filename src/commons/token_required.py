from src.models.users_model import Users
import jwt
from main import app
from flask import jsonify,request
from functools import wraps
def token_required(f):
    users_model=Users()
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            scheme=token.split(' ')[0]
            token=token.split(' ')[1]
        # return 401 if token is not passed
        if scheme!='Bearer':
            return jsonify({'message' : 'Invalid scheme !!'}), 401
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = users_model.find_one({"public_id":data["public_id"]})
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated