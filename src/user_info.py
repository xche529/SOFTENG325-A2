class User(object):
    def __init__(self, name, password):
        self.name = name
        self.messages_to_send = []
        self.password = password
        self.friends = {}
        self.client = None
        self.isOnline = False
        
        
    def add_friend(self, friend):
        self.friends[friend.name] = (friend)
        print("Friend added: ", friend.name)
        
    def remove_friend(self, friend):
        self.friends[friend.name].pop()
        print("Friend removed: ", friend.name)
    
    def add_message(self, message):
        self.messages_to_send.append(message)
        
    def get_message(self):
        if len(self.messages_to_send) == 0:
            return False
        else:
            return self.messages_to_send.pop(0)
        
    def build_message(self, message):
        return self.name + ": " + message
    
    def set_client(self, client):
        self.client = client
        
    def login(self, client):
        self.isOnline = True
        self.client = client
        print("User logged in: ", self.name)

    def logout(self):
        self.isOnline = False
        self.client = None
        print("User logged out: ", self.name)
    