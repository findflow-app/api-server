import jwt
import bcrypt
import mysql.connector
from flask import jsonify
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import re
from auth import auth


load_dotenv()
conn = None
cursor = None

SECRET_KEY = os.environ.get('SECRET_KEY')

# DB
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

def log_user(token, beacon_mac):
    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    user_id = decoded.get('user_id')
    sql = "SELECT beacon_mac FROM log_user WHERE userID = %s ORDER BY time DESC LIMIT 1"
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(sql, (user_id,))
    result = cursor.fetchone()
    if result is not None:
        if result[0] == beacon_mac:
            cursor.close()
            conn.close()
            return jsonify({'status': 'error', 'message': 'Already logged'}), 200
        else:
            cursor.execute("INSERT INTO log_user (userID, beacon_mac) VALUES (%s, %s)", (user_id, beacon_mac))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({'status': 'success'}), 200
    else:
        cursor.execute("INSERT INTO log_user (userID, beacon_mac) VALUES (%s, %s)", (user_id, beacon_mac))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success'}), 200

def search_user(token, name_string):
    userdata = auth(token)
    if userdata == "error" or userdata is None:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
    else:
        if len(name_string.split(' ')) == 1:
            name = name_string
            surname = ''
        else:
            name, surname = name_string.split(' ', 1)
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT id,name FROM users WHERE name LIKE %s AND name LIKE %s", ("%" + name + "%", "%" + surname + "%"))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'result': result}), 200
    
def get_user_position(token, user_id):
    userdata = auth(token)
    if userdata == "error" or userdata is None:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT log_user.beacon_mac, beacons.type,  FROM log_user WHERE userID = %s ORDER BY time DESC LIMIT 1", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success', 'mac': result}), 200