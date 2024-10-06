import socket


class Client(object):
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        print("Client connected to server")
        
    def send_message(self, message):
        message = message.encode('utf-8')
        message_len = len(message)
        send_len = str(message_len).encode('utf-8')
        send_len += b' ' * (1024 - len(send_len))
        self.client.send(send_len)
        self.client.send(message)
        
    def receive_message(self):
        message_len = self.client.recv(1024).decode('utf-8')
        if message_len:
            message_len = int(message_len)
            message = self.client.recv(message_len).decode('utf-8')
            print(message)
            
    def close(self):
        self.client.close()
        print("Client disconnected from server")
        
    def run(self):
        while True:
            message = input("Enter message: ")
            self.send_message(message)
            self.receive_message()

if __name__ == '__main__':
    port = int(input("Enter port: "))
    client = Client('localhost', port)
    client.run()
    client.close()