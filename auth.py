import jwt
import bcrypt
import mysql.connector
from flask import jsonify
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv


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

def auth(email, password):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    sql = "SELECT id, password FROM users WHERE email = %s"
    cursor.execute(sql, (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result is None or not bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
        return jsonify({'status': 'error', 'message': 'User auth failed: wrong email or password'}), 401
    else:
        #JWT 
        payload = {
            'user_id': result[0]
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token


def register(email, password, name, phone_number=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
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

        token = auth(email, password)
    return jsonify({'status': 'success', 'message': 'User registered successfully', 'token': token})
