import socket
from utils import *

class Client(object):
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.connected = False
        print("Client connected to server")
                    
    def close(self):
        self.client.close()
        print("Client disconnected from server")
        
    def run(self):
        while True:
            message = input("Enter message: ")
            if message == "!exit":
                send_message(message)
                break
            send_message(self.client, message)
            recieve_message(self.client)
            
    def welcome(self):
        command = input("Please type r to register or l to login: ")
        if command == "r":
            name = input("Please enter a username: ")
            password = input("Please enter a password: ")
            message = "!register"
            send_message(self.client, message)
            register_message = name + " " + password
            send_message(self.client,register_message)
            result = recieve_message(self.client)
            print(result)
            [is_success, message] = result.split("#")
            is_success = bool(is_success)
            print(message)
            
        elif command == "l":
            name = input("Please enter your username: ")
            password = input("Please enter your password: ")
            message = "!login"
            send_message(self.client, message)
            login_message = name + " " + password
            send_message(self.client,login_message)
            result = recieve_message(self.client)
            [is_success, message] = result.split("#")
            is_success = bool(is_success)
            print(message)

    def select_user(self):
        name = input("Please enter the name of the user you would like to message: ")
        name = name.trim()
        send_message(self.client, name)
        result = recieve_message(self.client)
        [is_success, message] = result.split(" ")
        is_success = bool(is_success)
        print(message)
            
            
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
