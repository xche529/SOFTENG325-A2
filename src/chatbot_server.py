import socket
import ssl
import threading
from utils import *
from user_info import User
import pickle
from chatbot import chatbot

SERVER_HOST = '0.0.0.0'
FORMAT = 'utf-8'
class Server(object):
    def __init__(self, port):
        # create a new SSL context
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.load_cert_chain(certfile="cert.pem", keyfile="cert.pem")
        self.context.load_verify_locations("cert.pem")
        self.context.set_ciphers('AES128-SHA')
        # create a new server socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        self.server.settimeout(1)
        self.server = self.context.wrap_socket(self.server, server_side=True)
        self.running_thread = []
        self.running = False
        try:
            # load the user map from a pickle file
            self.user_map = pickle.load(open("user_map.pickle", "rb"))
        except Exception as e:
            print("Error loading user map: ", e)
            print("Creating new empty user map")
            self.user_map = {}
        print("Server initlised, listening on port ", port)
    
    # stop the server
    def stop(self):
        self.running = False
        self.server.close()
        for thread in self.running_thread:
            thread.join()
        self.remove_socket_from_usermap()
        # save the user map to a pickle file
        pickle.dump(self.user_map, open("user_map.pickle", "wb"))
        print("Server stopped")

    # handle client connection
    def handle_client(self, client, address):
        print("Client connected: ", address)
        client.settimeout(1)
        connected = True
        while connected and self.running:
            try:
                message = recieve_message(client)
                if message:
                    print('\n')
                    print(f"[{address}]: {message}")
                    print('\n')
                    if message == "!disconnect":
                        connected = False
                        print("Client disconnected: ", address)
                    elif message == "!login":
                        self.handle_login(client)
                    elif message == "!register":
                        self.handle_register(client)         
                    else:
                        self.handle_undefined(client)
                else:
                    continue
            except socket.timeout:
                continue
            except Exception as e:
                print("Error: ", e)
                connected = False
        client.close()
        print("Client connection closed: ", address)
        
    # handle login request from the client
    def handle_login(self, client):
        login_message = recieve_message(client)
        is_success, message, user = self.login_user(login_message, client)
        print(message)
        result_message = str(is_success) + "#" + message
        send_message(client, result_message)
        if is_success:
            # store the client socket in the user object
            user.set_client(client)
            # send message history
            self.handle_get_message_history(user)
            
            while user.isOnline and self.running:
                client.settimeout(None)
                message = recieve_message(client)
                if message:
                    if message == "!logout":
                        self.handle_logout(user.name)
                    # client request to select a user
                    elif message == "!select":
                        self.handle_select_user(client, user)
                    else:
                        return
        
    # handle logout request from the client
    def handle_logout(self, username):
        user = self.check_user_exists(username)
        if user:
            user.logout()
            print("User logged out: ", user.name)
        else:
            print("User does not exist")
        
    # handle register request from the client
    def handle_register(self, client):
        register_message = recieve_message(client)
        is_success, message = self.register_user(register_message)
        print(message)
        result_message = str(is_success) + "#" + message
        send_message(client, result_message)
    
    # handle undefined request from the client
    def handle_undefined(self, client):
        result_message = str(False) + "#" + "Invalid command"
        send_message(client, result_message)
        
    # handle select user request from the client
    def handle_select_user(self, client, user):
        is_success = False
        message = recieve_message(client)
        target_user = self.check_user_exists(message)
        if target_user:
            is_success = True
            if target_user.isOnline:
                message = "User is online"
            else:
                message = "User is offline, message will be sent when user is online"
        else:
            if message == "chatbot":
                is_success = True
                message = "Chatbot session started"
                
                result_message = str(is_success) + "#" + message
                send_message(client, result_message)
                self.handle_chatbot_session(user)
                return
            if message == "!list":
                message = self.return_users_string()
            else:
                message = "User does not exist"
        result_message = str(is_success) + "#" + message
        send_message(client, result_message)
        if not is_success:
            return
        else:
            self.start_chat(user, target_user)

    # check if the user password is correct
    def check_user_password(self, user, password):
        if user.password == password:
            return True
        return False
        
    # check if the user exists
    def check_user_exists(self, name):
        if name in self.user_map:
            return self.user_map[name]
        return False
    
    # register logic
    def register_user(self, message):
        register_success = False
        error_message = ''
        [name, password] = message.split(" ")
        if not self.check_user_exists(name):
            # create a new user object
            user = User(name, password)
            self.user_map[user.name] = user
            register_success = True
            error_message = "User added: " + user.name
        else:
            error_message = "User already exists"
        return register_success, error_message

    # login logic
    def login_user(self, message, client):
        login_success = False
        error_message = ''
        [name, password] = message.split(" ")
        user = self.check_user_exists(name)
        if user:
            if self.check_user_password(user, password):
                user.login(client)
                login_success = True
                error_message = "User login success: " + user.name
            else:
                error_message = "Invalid password"
        else:
            error_message = "User does not exist"
        return login_success, error_message, user
    
    # start chat session between two users
    def start_chat(self, user, target_user):
        while user.isOnline and self.running:
            message = recieve_message(user.client)
            if message:
                if message == "!logout": 
                    self.handle_logout(user.name)
                else:
                    self.handle_send_message(user, target_user, message)

    # send message from one user to another
    def handle_send_message(self, user, target_user, message):
        # build message (sender name + message)
        message = user.build_message(message)
        if target_user.isOnline:
            send_message(target_user.client, message)
            print("Message sent from: ", user.name, " to: ", target_user.name)
            print("Message: ", message)
        else:
            target_user.add_message(message)
            print("Message added to queue: ", message)
            
    # get message history for the user and send to the client
    def handle_get_message_history(self, user):
        message_record = user.get_message()
        if message_record:
            initial_message = "New Messages: "
            send_message(user.client, initial_message)
            while message_record:
                send_message(user.client, message_record)
                message_record = user.get_message()
        
        send_message(user.client, "!end")
    
    # chatbot session
    def handle_chatbot_session(self, user):
        print("Chatbot session started1")
        chatbot_session = chatbot()
        print("Chatbot session started")
        botuser = User("chatbot", 0000)
        while user.isOnline and self.running:
            message = recieve_message(user.client)
            if message:
                if message == "!logout": 
                    self.handle_logout(user.name)
                else:
                    response = self.chatbot_message_request(chatbot_session, message)
                    self.handle_send_message(botuser, user, response)
                    
    # handle chatbot message request
    def chatbot_message_request(self, chatbot, message):
        try:
            response = chatbot.get_response(message)
        except Exception as e:
            response = "Chatbot error: " + str(e)
        return response
            
    # main server loop
    def run(self):
        self.running = True
        self.server.listen(5)
        while self.running:
            try:
                client, address = self.server.accept()
                # create a new thread to handle the client
                thread = threading.Thread(target=self.handle_client, args=(client, address))
                self.running_thread.append(thread)
                thread.start()
            except socket.timeout:
                continue
            
    # remove all sockets from the user map for server shutdown
    def remove_socket_from_usermap(self):
        for user in self.user_map:
            self.user_map[user].client = None
        print("All users disconnected")
        
    # return all users in the user map as a string
    def return_users_string(self):
        result = "Avaliable users: \n"
        for user in self.user_map:
            result += user + "\n"
        return result


if __name__ == '__main__':
    port = int(input("Enter port number: "))
    server = Server(port)
    try:
        server.run()
    except KeyboardInterrupt:
        print("Server stopping...")
        server.stop()