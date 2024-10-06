

FORMAT = 'utf-8'

def recieve_message(socket):
    message_len = socket.recv(1024).decode(FORMAT)
    if message_len:
        message_len = int(message_len)
        message = socket.recv(message_len).decode(FORMAT)
        return message
    return None

def send_message(socket, message):
    message = message.encode('utf-8')
    message_len = len(message)
    send_len = str(message_len).encode('utf-8')
    send_len += b' ' * (1024 - len(send_len))
    socket.send(send_len)
    socket.send(message)
