class User(object):
    def __init__(self, name, password):
        self.name = name
        self.messages_to_send = []
        self.password = password
        self.friends = {}
        
        
    def add_friend(self, friend):
        self.friends[friend.name] = (friend)
        print("Friend added: ", friend.name)
        
    def remove_friend(self, friend):
        self.friends[friend.name].pop()
        print("Friend removed: ", friend.name)
        
    