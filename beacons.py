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
    array_info = []
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    for mac in array_mac:
        cursor.execute("SELECT type,data,data_type FROM beacons WHERE mac_address = %s", (mac,))
        result = cursor.fetchone()
        if result:
            array_info.append({
                'mac': mac,
                'name': result[0],
                'data_type': result[2],
                'data': result[1]
            })
        else:
            array_info.append({
                'mac': mac,
                'name': None,
                'data_type': None,
                'data': None
            })
    cursor.close()
    conn.close()
    
    response = {info['mac']: {'name': info['name'], 'data_type': info['data_type'], 'data': info['data']} for info in array_info}
    
    return jsonify(response), 200