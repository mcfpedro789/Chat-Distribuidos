import os
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import threading
from socketserver import ThreadingMixIn
from users_rooms import (
    load_data,  
    register_user, authenticate_user, create_room,
    get_room_list, authenticate_room, add_message_to_room,
    get_messages_from_room, sync_data_from_master, get_users, get_rooms
)
import requests

PRIMARY_SERVER = False  # Set to False for the replica server
REPLICA_SERVER_URL = "https://3884-2804-14d-5e81-82ef-e0c1-1f55-f44a-597c.ngrok-free.app"

def reload_data():
    """Função para recarregar dados periodicamente."""
    while True:
        print("Reloading data from JSON files...")
        load_data()
        time.sleep(1)  # Espera 10 segundos antes de recarregar novamente

# Inicia a thread para recarregar os dados
threading.Thread(target=reload_data, daemon=True).start()

print(f"Users on startup: {get_users()}")
print(f"Rooms on startup: {get_rooms()}")

class ChatHandler(SimpleHTTPRequestHandler):
    """Handles HTTP requests for chat application."""
    
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        super().end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        if self.path == '/register':
            username = data.get('username')
            password = data.get('password')
            if register_user(username, password):
                self.send_response(200)
            else:
                self.send_response(409)  # Conflict
            self.end_headers()
        
        elif self.path == '/login':
            username = data.get('username')
            password = data.get('password')
            if authenticate_user(username, password):
                self.send_response(200)
            else:
                self.send_response(401)  # Unauthorized
            self.end_headers()

        elif self.path == '/create_room':
            room_name = data.get('room_name')
            room_password = data.get('room_password')

            if not room_name or not room_password:
                self.send_response(400)
                self.end_headers()
                return

            print(f"Creating room: {room_name} with password: {room_password}")

            if create_room(room_name, room_password):
                self.send_response(200)
            else:
                self.send_response(409)  # Conflict
            self.end_headers()

        elif self.path == '/join_room':
            room_name = data.get('room_name')
            room_password = data.get('room_password')

            if authenticate_room(room_name, room_password):
                self.send_response(200)
            else:
                self.send_response(401)  # Unauthorized
            self.end_headers()
        
        elif self.path == '/send':
            room_name = data.get('room_name')
            user_id = data.get('user_id')
            message = data.get('message')

            if not all([room_name, user_id, message]):
                self.send_response(400)
                self.end_headers()
                return

            log_message = f"User {user_id}: {message}"
            print(f"Received message: {log_message}")
            add_message_to_room(room_name, log_message)
            self.send_response(200)
            self.end_headers()
        
        elif self.path.startswith('/sync'):
            data_type = self.path.split('/')[-1]
            if data_type == 'users':
                sync_data_from_master('users', data)
            elif data_type == 'rooms':
                sync_data_from_master('rooms', data)
            self.send_response(200)
            self.end_headers()

        else:
            self.send_error(404, "File not found")

    def sync_with_replica(self, endpoint, data):
        try:
            response = requests.post(f"{REPLICA_SERVER_URL}{endpoint}", json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to sync with replica: {e}")

    def do_GET(self):
        if self.path.startswith('/messages'):
            query_components = self.parse_query_string()
            room_name = query_components.get('room_name')
            if room_name:
                messages = get_messages_from_room(room_name)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(messages).encode())
            else:
                self.send_error(400, "Bad Request")
        elif self.path == '/rooms':
            room_list = get_room_list()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(room_list).encode())
        else:
            super().do_GET()

    def parse_query_string(self):
        from urllib.parse import urlparse, parse_qs
        query = urlparse(self.path).query
        return {k: v[0] for k, v in parse_qs(query).items()}

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def run(server_class=ThreadedHTTPServer, handler_class=ChatHandler, port=8080):
    os.chdir('C:/Users/pedro/Desktop/Chat/client')
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
