from flask import Blueprint,send_from_directory
get_file1 = Blueprint('get_file', __name__)
@get_file1.route('/file/<path:path>',methods=['GET'])
def send_report(path):
    return send_from_directory('file', path)