from flask import Flask, request, jsonify, redirect
import os
from datetime import datetime
from dotenv import load_dotenv
import mysql.connector
import bcrypt
import ssl
import jwt
from auth import *
from log_user import *
from flask_cors import CORS, cross_origin
from beacons import *


load_dotenv()



app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

conn = None
 
# DB
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}
@app.route('/login', methods=['POST'])
@cross_origin()
def login_endpoint():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if (email is None) or (password is None):
        return jsonify({'status': 'error', 'message': 'Missing parameters'}), 400
    else:
        token = login(email, password) 
        if(token == 'error'):
            return jsonify({'status': 'error', 'message': 'User not found'}), 401
        else:
            return jsonify({'status': 'success', 'token': token }), 200           



@app.route('/register', methods=['POST'])
@cross_origin()
def register_endpoint():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    phone_number = data.get('phone_number')

    if (email is None) or (password is None) or (name is None):
        return jsonify({'status': 'error', 'message': 'Missing parameters'}), 400
    else:
       return register(email, password, name, phone_number)


@app.route('/auth', methods=['POST'])
@cross_origin()
def auth_endpoint():
    data = request.get_json()
    token = data.get('token')
    return auth(token)

@app.route('/info', methods=['GET'])
def test():
    return jsonify({'status': 'success',
                    'time': datetime.now(),
                    'version': os.getenv("VERSION")}
                    ), 200

"""@app.route('/beacons', methods=['GET'])
def get_beacons():"""

@app.route('/log_user', methods=['POST'])
@cross_origin()
def log_user_handle():
    data = request.get_json()
    token = data.get('token')
    beacon_id = data.get('beacon_id')
    return log_user(token, beacon_id)

@app.route('/beacon', methods=['POST'])
@cross_origin()
def get_beacon_endpoint():
    data = request.get_json()
    token = data.get('token')
    beacon_mac = data.get('beacon_mac')
    return get_beacon(token, beacon_mac)

@app.route('/search', methods=['POST'])
@cross_origin()
def search_user_endpoint():
    data = request.get_json()
    token = data.get('token')
    name_string = data.get('name_string')
    return search_user(token, name_string)

@app.route('/beacon_names', methods=['POST'])
@cross_origin()
def beacon_names_endpoint():
    data = request.get_json()
    array_mac = data.get('array_mac')
    return beacon_names(array_mac)

@app.route('/get_position', methods=['POST'])
@cross_origin()
def get_user_position_endpoint():
    data = request.get_json()
    token = data.get('token')
    user_id = data.get('user_id')
    return get_user_position(token, user_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    os.system('cls' if os.name == 'nt' else 'clear')
