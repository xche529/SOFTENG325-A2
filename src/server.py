import socket




SERVER_HOST = 'localhost'

class Server(object):
    def __init__(self, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        self.server.listen(5)
        print("Server started, listening on port ", port)

    def run(self):
        while True:
            connection, address = self._socket.accept()
            self._handle(connection)

