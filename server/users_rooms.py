import json
import os

# User data structure
users = {}
# Room data structure
rooms = {}

# Load existing data from JSON files
if os.path.exists('users.json'):
    with open('users.json', 'r') as f:
        users = json.load(f)

if os.path.exists('rooms.json'):
    with open('rooms.json', 'r') as f:
        rooms = json.load(f)

def save_users():
    with open('users.json', 'w') as f:
        json.dump(users, f)

def save_rooms():
    with open('rooms.json', 'w') as f:
        json.dump(rooms, f)

def register_user(username, password):
    if username in users:
        return False
    users[username] = {'password': password}
    save_users()
    return True

def authenticate_user(username, password):
    return username in users and users[username]['password'] == password

def create_room(room_name, room_password):
    if room_name in rooms:
        return False
    rooms[room_name] = {'password': room_password, 'messages': []}
    save_rooms()
    return True

def get_room_list():
    return list(rooms.keys())

def authenticate_room(room_name, room_password):
    return room_name in rooms and rooms[room_name]['password'] == room_password

def add_message_to_room(room_name, message):
    if room_name in rooms:
        rooms[room_name]['messages'].append(message)
        save_rooms()

def get_messages_from_room(room_name):
    if room_name in rooms:
        return rooms[room_name]['messages']
    return []
