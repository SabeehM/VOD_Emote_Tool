from twitch import Helix
from twitch.helix import Video
from chat import Chat, Message

class HelixClient:
    def __init__(self, clientID: str, bearer_token: str):
        self.helixClient =  Helix(client_id=clientID, bearer_token=bearer_token, use_cache=True)
        self.commentData : Chat = Chat()
    def getVideoData(self, videoID: str):
        foundVideo = self.helixClient.videos([videoID])[0]
        for comment in (foundVideo.comments):
            currentData = comment.data
            emoticonInfo : dict() = dict()

            for emoteIndex in range(len(currentData.get("message", None).get("emoticons", []))):
                id = (currentData.get("message", None).get("emoticons", [])[emoteIndex]['_id'])
                emoticonInfo[id] = self.commentData.cached(id)
                if(not emoticonInfo[id]):
                    start = currentData.get("message", None).get("emoticons", [])[emoteIndex]['begin']
                    end = currentData.get("message", None).get("emoticons", [])[emoteIndex]['end']
                    emoticonInfo[id] = currentData.get("message", None).get("body", None)[start:end+1]

            self.commentData.add(
                Message(
                currentData['commenter']['name'], 
                currentData['created_at'], 
                currentData['message']['body'],
                emoticonInfo
                )
            )
    def emoteAnalysis(self):
        return