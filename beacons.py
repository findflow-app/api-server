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

# DB
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}

def beacon_names(array_mac):
    array_name = []
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    for mac in array_mac:
        cursor.execute("SELECT type FROM beacons WHERE mac_address = %s", (mac,))
        result = cursor.fetchone()
        if result:
            array_name.append(result[0])
        else:
            array_name.append(None)
    cursor.close()
    conn.close()
    response = []
    for mac, name in zip(array_mac, array_name):
        response.append({ mac : name, )
    
    return jsonify(response), 200