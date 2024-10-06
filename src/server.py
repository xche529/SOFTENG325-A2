import socket
import threading
from utils import *
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
            message = recieve_message(client)
            if message:
                print(f"[{address}]: {message}")
                if message == "exit":
                    connected = False
                    print("Client disconnected: ", address)
                    
                elif message == "login":
                    login_message = recieve_message(client)
                    is_success, message = self.login_user(login_message)
                    print(message)
                    send_message(client, message)

                elif message == "register":
                    register_message = recieve_message(client)
                    is_success, message = self.register_user(register_message)
                    print(message)
                    send_message(client, message)
                    
                else:
                    user = self.check_user_exists(message)
                    if user:
                        if user.isOnline:
                            print("User is online")
                        else:
                            print("User is offline")
                    else:
                        print("User does not exist")
            else:
                connected = False
                print("Client disconnected: ", address)
                    
    def check_user_password(self, user, password):
        if user.password == password:
            return True
        return False
        
                    
    def check_user_exists(self, name):
        if name in self.user_map:
            return self.user_map[name]
        return False
                    
    def register_user(self, message):
        register_success = False
        error_message = ''
        [name, password] = message.split(" ")
        if not self.check_user_exists(name):
            user = User(name, password)
            self.user_map[user.name] = user
            register_success = True
            error_message = "User added: " + user.name
        else:
            error_message = "User already exists"
        return register_success, error_message

    def login_user(self, message):
        login_success = False
        error_message = ''
        [name, password] = message.split(" ")
        user = self.check_user_exists(name)
        if user:
            if self.check_user_password(user, password):
                user.isOnline = True
                login_success = True
                error_message = "User login success: " + user.name
            else:
                error_message = "Invalid password"
        else:
            error_message = "User does not exist"
        return login_success, error_message
        
        
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
