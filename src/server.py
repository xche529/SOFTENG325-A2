import socket




SERVER_HOST = 'localhost'

class Server(object):
    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        self.server.listen(5)
        self.user_map = {}
        print("Server initlised, listening on port ", port)
        
        
    def stop(self):
        self.server.close()
        print("Server stopped")
        
        
    def add_user(self, client, address):
        self.user_map[user.name] = user
        print("User added: ", user.name)


    def run(self):
        while True:
            client, address = self.server.accept()
            thread = threading.Thread(target=self.add_user, args=(client, address))
            print("Connection from: ", address)
            client.send(b'Hello, you are connected to the server\n')
            client.close()

