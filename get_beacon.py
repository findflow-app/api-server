from auth import auth
from flask import jsonify
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

# DB
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'database': os.getenv('DB_NAME')
}




def get_beacon(token, beacon_mac):
    userdata = auth(token)
    print(1)
    if userdata == "error" or userdata is None:
        return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
    print(1.1)
    user_id = userdata['id']
    print(2)
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    sql = "SELECT * FROM beacons WHERE mac_address = %s"
    cursor.execute(sql, (beacon_mac,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    print(3)
    if result is None:
        return jsonify({'status': 'error', 'message': 'Beacon not found'}), 404
    else:
        beacon_ID = result[0]
        print(4)
        institution_id = result[2]
        beacon_lat = result[3]
        beacon_lon = result[4]
        beacon_radius = result[5]
        beacon_type = result[6]
        beacon_area = result[7]
        sql = "SELECT * FROM conn_institutions_users WHERE user = %i AND institution = %i"
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(sql, (user_id, institution_id))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result is None:
            return jsonify({'status': 'error', 'message': 'User not authorized to access this beacon'}), 401
        else:
            institution_role = result[3]
            sql = "SELECT * FROM institutions WHERE id = %i"
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(sql, (institution_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            institution_name = result[1]
            institution_email = result[2]
            institution_website = result[3]
            institution_phone_number = result[4]
            institution_address = result[5]
            institution_zip_code = result[6]
            institution_country = result[7]
            print(5)
            sql = "SELECT * FROM areas WHERE id = %i"
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(sql, (beacon_area,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            room_id = result[1]
            area_x = result[2]
            area_y = result[3]
            area_width = result[5]
            area_height = result[6]
            print(6)
            sql = "SELECT * FROM rooms WHERE id = %i"
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(sql, (room_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            room_name = result[1]
            room_description = result[2]
            room_organization = result[3]
            room_floor = result[4]
            print(7)
            sql = "SELECT * FROM conn_events_rooms WHERE room = %i"
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute(sql, (beacon_area,))
            result = cursor.fetch()
            cursor.close()
            conn.close()
            events = []
            for event in result:
                print(7)
                event_id = event[1]
                sql = "SELECT * FROM events WHERE id = %i"
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute(sql, (event_id,))
                result = cursor.fetchone()
                cursor.close()
                conn.close()
                if(event[2] == 1):
                    event_type = event[1]
                    event_data = event[4]             
                
                events.append(event)
            return jsonify({'status': 'success', 'beacon': {'id': beacon_ID, 'mac_address': beacon_mac, 'lat': beacon_lat, 'lon': beacon_lon, 'radius': beacon_radius, 'type': beacon_type, 'area': {'id': beacon_area, 'x': area_x, 'y': area_y, 'width': area_width, 'height': area_height, 'room': {'id': room_id, 'name': room_name, 'description': room_description, 'organization': room_organization, 'floor': room_floor, 'events': events}}, 'institution': {'id': institution_id, 'name': institution_name, 'email': institution_email, 'website': institution_website, 'phone_number': institution_phone_number, 'address': institution_address, 'zip_code': institution_zip_code, 'country': institution_country}}}), 200






    
    
    