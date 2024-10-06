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
                if message == "exit":
                    connected = False
                if message == "login":
                    self.login(client, address)
                elif message == "register":
                    self.register(client, address)
                    
                    
    def check_user_password(self, user, password):
        if user.password == password:
            return True
        return False
        
                    
    def check_user_exists(self, name):
        if name in self.user_map:
            return self.user_map[name]
        return False
                    
    def add_user(self, message):
        [name, password] = message.split(" ")
        if not self.check_user_exists(name):
            user = User(name, password)
            self.user_map[user.name] = user
            print("User added: ", user.name)
            return True
        else:
            print("User already exists")
            return False

    def login_user(self, message):
        [name, password] = message.split(" ")
        user = self.check_user_exists(name)
        if user:
            if self.check_user_password(user, password):
                user.isOnline = True
                print("User logged in: ", user.name)
                return True
            else:
                print("Invalid password")
                return False
        else:
            print("User does not exist")
            return False
        
        
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
