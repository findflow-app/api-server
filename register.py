import bcrypt
import mysql.connector
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from auth import auth


load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}



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

        return jsonify({'status': 'success', 'message': 'User registered successfully', 'token': token}), 201