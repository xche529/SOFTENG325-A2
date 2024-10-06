import socket
import threading

from user_info import User




SERVER_HOST = 'localhost'
FORMAT = 'utf-8'
class Server(object):
    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        self.user_map = {}
        print("Server initlised, listening on port ", port)


    def stop(self):
        self.server.close()
        print("Server stopped")

    def handle_client(self, client, address):
        print("Client connected: ", address)
        
        connected = True
        while connected:
            message_len = client.recv(1024).decode(FORMAT)
            if message_len:
                message_len = int(message_len)
                message = client.recv(message_len).decode(FORMAT)
                print(f"[{address}]: {message}")
                
    def add_user(self, client, address):
        user = User(client, address)
        self.user_map[user.name] = user
        print("User added: ", user.name)


    def run(self):
        self.server.listen(5)
        while True:
            client, address = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(client, address))
            thread.start()

if __name__ == '__main__':
    port = int(input("Enter port number: "))
    server = Server(port)
    server.run()
