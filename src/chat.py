class Message:
    def __init__(self, commenter, date, message, emoticon):
        self.commenter = commenter
        self.date = date
        self.message = message
        self.emoticon = emoticon

class Chat:
    def __init__(self):
        self.messages : list = []
        self.cache: dict() = dict()
    def add(self, message: Message):
        for ID in message.emoticon.keys():
            self.cache[ID] = message.emoticon[ID]
        self.messages.append(message)
    def cached(self, key):
        return self.cache.get(key, None)
    
