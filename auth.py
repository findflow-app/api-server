import jwt
import bcrypt
import mysql.connector
from flask import jsonify
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import re


load_dotenv()

# Secret key for encoding the JWT
SECRET_KEY = os.environ.get('SECRET_KEY')

# DB
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

def login(email, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        sql = "SELECT id, password FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result is None or not bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
            return 'error'
        else:
            #JWT 
            payload = {
                'user_id': result[0]
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return token
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


def register(email, password, name, phone_number=None):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        def is_valid_email(email):
            regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            return re.match(regex, email)

        if not is_valid_email(email):
            cursor.close()
            conn.close()
            return jsonify({'status': 'error', 'message': 'Invalid email format'}), 400
        sql = "SELECT * FROM users WHERE email = %s"
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result is not None:
            cursor.close()
            conn.close()
            return jsonify({'status': 'error', 'message': 'User already exists'}), 400
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            if phone_number:
                sql = "INSERT INTO users (email, password, name, phone_number) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (email, hashed_password.decode('utf-8'), name, phone_number))
            else:
                sql = "INSERT INTO users (email, password, name) VALUES (%s, %s, %s)"
                cursor.execute(sql, (email, hashed_password.decode('utf-8'), name))
            conn.commit()
            cursor.close()
            conn.close()

            token = login(email, password)
        return jsonify({'status': 'success', 'message': 'User registered successfully', 'token': token})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def auth(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = decoded.get('user_id')    
        sql = "SELECT * FROM users WHERE id = %s"
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result is None:
            return 'error'
        id = result[0]
        email = result[1]
        name = result[2]
        phone_number = result[4]
        role = result[6]
        return jsonify({'id': id, 'email': email, 'name': name, 'phone_number': phone_number, 'role': role}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500