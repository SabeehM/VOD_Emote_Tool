from twitch import Helix
from twitch.helix import Video
from .chat import Chat, Message
from .analyzer import Analyzer
from .logger import Logger
from .stringUtil import StringUtil
from datetime import datetime, timedelta
import dateutil.parser

__defaultBase__ = 10

class HelixClient:
    def __init__(self, clientID: str, bearer_token: str) -> None:
        self.helixClient : Helix =  Helix(client_id=clientID, bearer_token=bearer_token, use_cache=False)
        self.commentData : Chat = Chat()
        self.commentAnalyzer : Analyzer = Analyzer()
        self.currentVideo : Video = None

    def getVideoData(self, videoID: str) -> None:
        self.currentVideo = self.helixClient.videos([videoID])[0]
        self.commentData.streamer = self.currentVideo.user_name
        self.commentData.startTime = dateutil.parser.parse(self.currentVideo.created_at)
        newduration : datetime = dateutil.parser.parse(self.currentVideo.duration)
        self.commentData.endTime = self.commentData.startTime + timedelta(hours = newduration.hour, minutes = newduration.minute, seconds = newduration.second)
        return

    def getCommentData(self) -> None:
        foundVideo : Video = self.currentVideo
        commentCount : int = 0
        for comment in (foundVideo.comments):
            currentData : dict() = comment.data
            emoticonInfo : dict() = dict()
            emotes : bool = False
            Logger.print_info('Extracted ' + str(commentCount) + ' messages...', end='\r')
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
        Logger.exit_line()
        Logger.print_pass("Completed...")
        return

    def searchExternalEmote(self, emoteName : str) -> None:
        foundVideo : Video = self.currentVideo
        commentCount : int = 0
        for comment in (foundVideo.comments):
            currentData : dict() = comment.data
            if(StringUtil.stringSearch(currentData['message']['body'], emoteName, __defaultBase__)):
                self.commentData.addExternal(
                    Message(
                        currentData['commenter']['name'], 
                        currentData['created_at'], 
                        currentData['message']['body'],
                        {"Ext": emoteName}
                    )
                )
            Logger.print_info('Seeked ' + str(commentCount) + ' messages...', end='\r')
            commentCount+=1
        Logger.exit_line()
        Logger.print_pass("Completed...")
        return

    def emoteAnalysis(self) -> None:
        self.commentAnalyzer.emoteSpread(self.commentData)
        return

    def emoteOverTime(self, emoteName : str, external : bool = False, timeSegments : int = None, suggestions : int = None) -> None:
        self.commentAnalyzer.emotePopularity(self.currentVideo, self.commentData, emoteName, external, timeSegments, suggestions)
        return