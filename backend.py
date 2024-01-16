from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data as a substitute for a real database
hostel_data = {
    'rooms': [
        {'id': 1, 'number': '101', 'occupant': None},
        {'id': 2, 'number': '102', 'occupant': None},
        # Add more rooms as needed
    ]
}

# API endpoint to get all rooms
@app.route('/rooms', methods=['GET'])
def get_rooms():
    return jsonify({'rooms': hostel_data['rooms']})

# API endpoint to get details of a specific room
@app.route('/rooms/<int:room_id>', methods=['GET'])
def get_room(room_id):
    room = next((room for room in hostel_data['rooms'] if room['id'] == room_id), None)
    if room:
        return jsonify({'room': room})
    else:
        return jsonify({'message': 'Room not found'}), 404

# API endpoint to allocate a room to a resident
@app.route('/allocate-room', methods=['POST'])
def allocate_room():
    data = request.get_json()
    room_id = data.get('room_id')
    resident_name = data.get('resident_name')

    room = next((room for room in hostel_data['rooms'] if room['id'] == room_id), None)

    if room and room['occupant'] is None:
        room['occupant'] = resident_name
        return jsonify({'message': f'Room {room_id} allocated to {resident_name}'})
    elif room:
        return jsonify({'message': f'Room {room_id} is already occupied'}), 400
    else:
        return jsonify({'message': 'Room not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
