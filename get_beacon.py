def get_beacon():
    data = request.get_json()
    token = data.get('token')
    if(not token):
        return jsonify({'status': 'error', 'message': 'Missing parameters'}), 400
    if(not )
    