import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import threading
from socketserver import ThreadingMixIn
from users_rooms import (
    register_user, authenticate_user, create_room,
    get_room_list, authenticate_room, add_message_to_room,
    get_messages_from_room
)

class ChatHandler(SimpleHTTPRequestHandler):
    """Handles HTTP requests for chat application."""
    
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
            log_message = f"User {user_id}: {message}"
            print(f"Received message: {log_message}")
            add_message_to_room(room_name, log_message)
            self.send_response(200)
            self.end_headers()
        
        else:
            self.send_error(404, "File not found")

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
    os.chdir('/home/julianafreitas/FURG/Chat/client')
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
