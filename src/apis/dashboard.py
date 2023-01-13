from flask import Blueprint,request
app1 = Blueprint('app', __name__)
@app1.route('/',methods=['GET'])
def dashboard():
    return "DASHBOARD"