import socket
import threading
from utils import *
from user_info import User
import pickle




SERVER_HOST = 'localhost'
FORMAT = 'utf-8'
class Server(object):
    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        self.server.settimeout(1)
        self.running_thread = []
        self.running = False
        try:
            self.user_map = pickle.load(open("user_map.pickle", "rb"))
        except FileNotFoundError:
            self.user_map = {}
        print(self.user_map.values())
        print("Server initlised, listening on port ", port)
        
    def stop(self):
        self.running = False
        for thread in self.running_thread:
            thread.join()
        self.server.close()
        pickle.dump(self.user_map, open("user_map.pickle", "wb"))
        print("Server stopped")

    def handle_client(self, client, address):
        print("Client connected: ", address)
        connected = True
        while connected and self.running:
            message = recieve_message(client)
            if message:
                print('\n')
                print(f"[{address}]: {message}")
                print('\n')
                if message == "!exit":
                    connected = False
                    print("Client disconnected: ", address)
                    
                elif message == "!login":
                    self.handle_login(client, message)
                elif message == "!register":
                    self.handle_register(client, message)            
                else:
                    self.handle_select_user(client, message)
            else:
                continue
        client.close()
        print("Client connection closed: ", address)
        
    def handle_login(self, client, message):
        login_message = recieve_message(client)
        is_success, message = self.login_user(login_message)
        print(message)
        result_message = str(is_success) + "#" + message
        send_message(client, result_message)

        
    def handle_register(self, client, message):
        register_message = recieve_message(client)
        is_success, message = self.register_user(register_message)
        print(message)
        result_message = str(is_success) + "#" + message
        send_message(client, result_message)
        
    def handle_select_user(self, client, message):
        user = self.check_user_exists(message)
        if user:
            if user.isOnline:
                print("User is online")
            else:
                print("User is offline")
        else:
            print("User does not exist")

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
        self.running = True
        self.server.listen(5)
        while self.running:
            try:
                client, address = self.server.accept()
                thread = threading.Thread(target=self.handle_client, args=(client, address))
                self.running_thread.append(thread)
                thread.start()
            except socket.timeout:
                continue


if __name__ == '__main__':
    port = int(input("Enter port number: "))
    server = Server(port)
    try:
        server.run()
    except KeyboardInterrupt:
        print("Server stopping...")
        server.stop()