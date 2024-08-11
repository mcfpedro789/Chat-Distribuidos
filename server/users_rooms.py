import json
import os

# User data structure
users = {}
# Room data structure
rooms = {}

# Defina o caminho correto para os arquivos JSON
BASE_DIR = os.path.join(os.path.dirname(__file__), '../client')  # Ajusta o caminho para o diretório client
USERS_FILE = os.path.join(BASE_DIR, 'users.json')
ROOMS_FILE = os.path.join(BASE_DIR, 'rooms.json')

# Load existing data from JSON files
def load_data():
    global users, rooms
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        print(f"Loaded users: {users}")
    else:
        print("No users.json file found.")
    
    if os.path.exists(ROOMS_FILE):
        with open(ROOMS_FILE, 'r') as f:
            rooms = json.load(f)
        print(f"Loaded rooms: {rooms}")
    else:
        print("No rooms.json file found.")

load_data()  # Carrega os dados ao iniciar o módulo

def save_users():
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f)
    print(f"Users saved: {users}")

def save_rooms():
    with open(ROOMS_FILE, 'w') as f:
        json.dump(rooms, f)
    print(f"Rooms saved: {rooms}")

def register_user(username, password):
    if username in users:
        return False
    users[username] = {'password': password}
    save_users()
    print(f"Registered new user: {username}")
    return True

def authenticate_user(username, password):
    return username in users and users[username]['password'] == password

def create_room(room_name, room_password):
    if room_name in rooms:
        return False
    rooms[room_name] = {'password': room_password, 'messages': []}
    save_rooms()
    print(f"Created new room: {room_name}")
    return True


def get_room_list():
    return list(rooms.keys())

def authenticate_room(room_name, room_password):
    if room_name in rooms:
        return rooms[room_name]['password'] == room_password
    return False


def add_message_to_room(room_name, message):
    if room_name in rooms:
        rooms[room_name]['messages'].append(message)
        save_rooms()
        print(f"Added message to room {room_name}: {message}")

def get_messages_from_room(room_name):
    if room_name in rooms:
        return rooms[room_name]['messages']
    return []

def get_users():
    return users

def get_rooms():
    return rooms

def sync_data_from_master(data_type, data):
    global users, rooms
    if data_type == 'users':
        users = data
        save_users()
    elif data_type == 'rooms':
        rooms = data
        save_rooms()
