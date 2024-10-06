import socket
import threading
from utils import *

class Client(object):
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.connected = False
        self.logged_in = False
        print("Client connected to server")
                    
    def close(self):
        self.connected = False
        self.client.close()
        print("Client disconnected from server")
        
    def listen_for_messages(self):
        while self.connected:
            message = recieve_message(self.client)
            if message:  
                print('\n')
                print(message)
        
    def start_chat(self):
        listen_thread = threading.Thread(target=self.listen_for_messages)
        listen_thread.start()
        while self.connected:
            message = input("Enter message: ")
            if message == "!disconnect":
                send_message(message)
                self.close()
            send_message(self.client, message)
            
    def welcome(self):
        self.connected = True
        while self.connected:
            command = input("Please type r to register or l to login: ")
            if command == "r":
                name = input("Please enter a username: ")
                password = input("Please enter a password: ")
                message = "!register"
                is_success = self.handle_auth_opeartion(message, name, password)
                
            elif command == "l":
                name = input("Please enter your username: ")
                password = input("Please enter your password: ")
                message = "!login"
                is_success = self.handle_auth_opeartion(message, name, password)
                if is_success:
                    self.logged_in = True
                    while self.logged_in:
                        self.select_user()
            else:
                print("Invalid command")
                print('\n')
                
    def handle_auth_opeartion(self, operation, name, password):
        send_message(self.client, operation)
        message = name + " " + password
        send_message(self.client,message)
        result = recieve_message(self.client)
        [is_success, message] = result.split("#")
        is_success = bool(is_success)
        print(message)
        return is_success
    
    def select_user(self):
        name = input("Please enter the name of the user you would like to message or l to logout: ")
        if name == "l":
            send_message(self.client, "!logout")
            self.logged_in = False
            return
        name = name.strip()
        send_message(self.client, "!select")
        send_message(self.client, name)
        result = recieve_message(self.client)
        [is_success, message] = result.split("#")
        is_success = bool(is_success)
        print(message)
        if is_success:
            self.start_chat()
            
            
if __name__ == '__main__':
    try:
        port = int(input("Enter port: "))
        client = Client('localhost', port)
        client.welcome()
        client.close()
    except KeyboardInterrupt:
        client.close()
    finally:
        client.close()
