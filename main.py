from flask import Flask,session
app = Flask(__name__)
app.secret_key = 'AAAAAAAaaaaaa!!!!!!'
from dotenv import load_dotenv
load_dotenv()
from src.apis.v1_0 import *


    
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)