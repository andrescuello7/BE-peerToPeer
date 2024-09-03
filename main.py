import socket
import threading
import json
import os
import sys

class Server:
    def __init__(self):
        self.host_connecteds = []
        self.sockets_connecteds = []
        self.start_server()
        self.connect_socket()

        # Listener for incoming messages from stdin
        threading.Thread(target=self.listen_stdin).start()

    def listen_stdin(self):
        while True:
            buffer = input()
            self.send_message(buffer)

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((os.getenv('HOST'), int(os.getenv('PORT'))))
        server.listen()

        print(f"Server constructor {os.getenv('HOST')}:{os.getenv('PORT')}")

        def handle_client(conn):
            while True:
                try:
                    buffer = conn.recv(1024)
                    if not buffer:
                        break
                    data = buffer.decode('utf-8')
                    try:
                        data_json = json.loads(data)
                        if isinstance(data_json, list):
                            self.connect_peers(data_json)
                        else:
                            self.connect_peer(data_json['host'], data_json['port'], data_json)
                            print(f"\x1b[32m[+]\x1b[0m {data_json['host']}:{data_json['port']}")
                    except json.JSONDecodeError:
                        print(f"\x1b[33m  - \x1b[0m {data}")
                except ConnectionResetError:
                    break

            print("Socket closed")
            conn.close()

        def accept_connections():
            while True:
                conn, _ = server.accept()
                threading.Thread(target=handle_client, args=(conn,)).start()

        threading.Thread(target=accept_connections).start()

    def connect_socket(self):
        try:
            connect = sys.argv[1].split(':')
            HIS_HOST = connect[0]
            HIS_PORT = int(connect[1])

            self.connect_peer(HIS_HOST, HIS_PORT, {'port': HIS_PORT, 'host': HIS_HOST}, {'port': os.getenv('PORT'), 'host': os.getenv('HOST')})
            print(f"\x1b[32m[+]\x1b[0m {HIS_HOST}:{HIS_PORT}")
        except IndexError:
            pass

    def connect_peer(self, host, port, data, my_credentials=None):
        try:
            _socket = socket.create_connection((host, port))
            if isinstance(data, list):
                self.host_connecteds.extend(data)
            else:
                self.host_connecteds.append(data)
            self.sockets_connecteds.append(_socket)
            _socket.sendall(json.dumps(my_credentials or self.host_connecteds).encode('utf-8'))
        except socket.error as e:
            print(f"Error connecting to {host}:{port} - {e}")

    def send_message(self, buffer):
        for _socket in self.sockets_connecteds:
            try:
                _socket.sendall(buffer.strip().encode('utf-8'))
            except socket.error as e:
                print(f"Error sending message: {e}")

    def connect_peers(self, data):
        for connection in data:
            is_current_host = connection['port'] == int(os.getenv('PORT'))
            is_valid_connection = connection.get('port') is not None and connection.get('host') is not None
            is_not_connected = not any(peer['port'] == connection['port'] and peer['host'] == connection['host'] for peer in self.host_connecteds)

            if not is_current_host and is_valid_connection and is_not_connected:
                self.connect_peer(connection['host'], connection['port'], data, {'port': os.getenv('PORT'), 'host': os.getenv('HOST')})

if __name__ == "__main__":
    Server()

