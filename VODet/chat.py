from datetime import datetime, timedelta

class Message:
    def __init__(self, commenter : str, date : str, message : str, emoticon : dict()):
        self.commenter : str = commenter
        self.date : str = date
        self.message : str = message
        self.emoticon : dict() = emoticon

class Chat:
    def __init__(self):
        self.streamer : str = None
        self.startTime : datetime = None
        self.endTime : datetime = None
        self.messages : list = []
        self.emoteMessages : list = []
        self.externalEmoteMessages: list = []
        self.cache: dict() = dict()

    def add(self, message: Message) -> None:
        for ID in message.emoticon.keys():
            self.cache[ID] = message.emoticon[ID]
        if(message.emoticon):
            self.emoteMessages.append(message)
        self.messages.append(message)

    def addExternal(self, message : str) -> None:
        self.externalEmoteMessages.append(message)

    def cached(self, key : str) -> str:
        return self.cache.get(key, None)
    
