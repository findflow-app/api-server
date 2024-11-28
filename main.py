from flask import Flask, request, jsonify, redirect
import os
from datetime import datetime
from dotenv import load_dotenv
import mysql.connector
import bcrypt
import ssl
import jwt
from auth import login, register, auth
from flask_cors import CORS, cross_origin


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
"""@app.route('/validation', methods=['POST'])
def handle_validation_post():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    key = data.get('api_key')

    if not email or not password or not key:
        return jsonify({'status': 'error', 'message': 'Missing parameters'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    sql = "SELECT ID, api_info FROM programs WHERE api_key = %s"
    cursor.execute(sql, (key,))

    app_result = cursor.fetchone()
    cursor.close()

    if app_result is None:
        return jsonify({'status': 'error', 'message': 'API key not found'}), 401
    else:
        sql = "SELECT key, valid_to, users.active, license.active, acces, passwd FROM license RIGHT JOIN users ON license.user_ID = users.ID WHERE email = %s AND program = %s"
        cursor = conn.cursor()
        cursor.execute(sql, (email, app_result[0]))

        result = cursor.fetchone()
        cursor.close()

        if result is None or not bcrypt.checkpw(password.encode('utf-8'), result[5].encode('utf-8')):
            return jsonify({'status': 'error', 'message': 'User not found'}), 601
        else:
            if (result[1] is not None):
                if(result[1] < datetime.now().date()):
                    return jsonify({'status': 'error', 'message': 'License expired'}), 602
            if(result[2] == 0):
                return jsonify({'status': 'error', 'message': 'User not active'}), 603
            if(result[3] == 0):
                return jsonify({'status': 'error', 'message': 'License not active'}), 604

            return jsonify({
                    'status': 'success',
                    'key': result[0],
                    'expire': result[1].isoformat() if result[1] else None,
                    'access': result[4],
                    'static': app_result[1],
                    'time': datetime.now().isoformat() 
            }), 200"""

"""@app.route('/grouplist', methods=['POST'])
def handle_post_group():
    data = request.json
    key = data.get('api_key')

    if not key:
        return jsonify({'status': 'error', 'message': 'Missing parameters'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    sql = "SELECT ID, api_info FROM programs WHERE api_key = %s"
    cursor.execute(sql, (key,))

    app_result = cursor.fetchone()
    cursor.close()

    if app_result is None:
        return jsonify({'status': 'error', 'message': 'API key not found'}), 401
    else:
        sql = "SELECT group FROM license WHERE program = %s"
        cursor = conn.cursor()
        cursor.execute(sql, (app_result[0],))

        result = cursor.fetchall()
        cursor.close()

        if result is None:
            return jsonify({'status': 'error', 'message': 'Group not found'}), 605
        else:
            return jsonify({
                'header': {
                    'status': 'success',
                    'time': datetime.now.value,
                },
                'groups': result
            }), 200"""

@app.route('/info', methods=['GET'])
def test():
    return jsonify({'status': 'success',
                    'time': datetime.now(),
                    'version': os.getenv("VERSION")}
                    ), 200

"""@app.route('/beacons', methods=['GET'])
def get_beacons():"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    os.system('cls' if os.name == 'nt' else 'clear')
