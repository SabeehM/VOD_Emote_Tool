from twitch import Helix
from twitch.helix import Video
from chat import Chat, Message
from analyzer import Analyzer
import dateutil.parser
from datetime import datetime, timedelta

class HelixClient:
    def __init__(self, clientID: str, bearer_token: str):
        self.helixClient =  Helix(client_id=clientID, bearer_token=bearer_token, use_cache=False)
        self.commentData : Chat = Chat()
        self.commentAnalyzer : Analyzer = Analyzer()

    def getVideoData(self, videoID: str):
        foundVideo = self.helixClient.videos([videoID])[0]
        self.commentData.startTime = dateutil.parser.parse(foundVideo.created_at)
        newduration = dateutil.parser.parse(foundVideo.duration)
        self.commentData.endTime = self.commentData.startTime + timedelta(hours = newduration.hour, minutes = newduration.minute, seconds = newduration.second)
        self.getCommentData(foundVideo)
        return

    def getCommentData(self, foundVideo):
        commentCount = 0
        for comment in (foundVideo.comments):
            currentData = comment.data
            emoticonInfo : dict() = dict()
            emotes = False
            print('Extracted ' + str(commentCount) + ' messages...', end='\r')
            for emoteIndex in range(len(currentData.get("message", None).get("emoticons", []))):
                emotes = True
                id = (currentData.get("message", None).get("emoticons", [])[emoteIndex]['_id'])
                emoticonInfo[id] = self.commentData.cached(id)
                if(not emoticonInfo[id]):
                    start = currentData.get("message", None).get("emoticons", [])[emoteIndex]['begin']
                    end = currentData.get("message", None).get("emoticons", [])[emoteIndex]['end']
                    emoticonInfo[id] = currentData.get("message", None).get("body", None)[start:end+1]
            if(emotes):
                self.commentData.add(
                    Message(
                    currentData['commenter']['name'], 
                    currentData['created_at'], 
                    currentData['message']['body'],
                    emoticonInfo
                    )
                )
            commentCount+=1
        print("\n")
        return

    def emoteAnalysis(self):
        self.commentAnalyzer.emoteSpread(self.commentData)
        return
    def emoteOverTime(self, emoteName):
        self.commentAnalyzer.emotePopularity(self.commentData, emoteName)
        return