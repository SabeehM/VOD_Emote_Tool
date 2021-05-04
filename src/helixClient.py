from twitch import Helix
from twitch.helix import Video
from chat import Chat, Message
from analyzer import Analyzer
from logger import Logger
from datetime import datetime, timedelta
from stringUtil import StringUtil
import dateutil.parser

__defaultBase__ = 10

class HelixClient:
    def __init__(self, clientID: str, bearer_token: str):
        self.helixClient =  Helix(client_id=clientID, bearer_token=bearer_token, use_cache=False)
        self.commentData : Chat = Chat()
        self.commentAnalyzer : Analyzer = Analyzer()
        self.currentVideo = None

    def getVideoData(self, videoID: str):
        self.currentVideo = self.helixClient.videos([videoID])[0]
        self.commentData.startTime = dateutil.parser.parse(self.currentVideo.created_at)
        newduration = dateutil.parser.parse(self.currentVideo.duration)
        self.commentData.endTime = self.commentData.startTime + timedelta(hours = newduration.hour, minutes = newduration.minute, seconds = newduration.second)
        return

    def getCommentData(self):
        foundVideo = self.currentVideo
        commentCount = 0
        for comment in (foundVideo.comments):
            currentData = comment.data
            emoticonInfo : dict() = dict()
            emotes = False
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

    def searchExternalEmote(self, emoteName):
        foundVideo = self.currentVideo
        commentCount = 0
        for comment in (foundVideo.comments):
            currentData = comment.data
            #if(emoteName in currentData['message']['body']):
            if(StringUtil.stringSearch(currentData['message']['body'], emoteName, __defaultBase__)):
                self.commentData.addExternal(
                    Message(
                        currentData['commenter']['name'], 
                        currentData['created_at'], 
                        currentData['message']['body'],
                        {"Ext": emoteName}
                    )
                )
            '''
            Rabin-Karp algorithm
            '''
            Logger.print_info('Seeked ' + str(commentCount) + ' messages...', end='\r')
            commentCount+=1
        Logger.exit_line()
        Logger.print_pass("Completed...")
        return

    def emoteAnalysis(self):
        self.commentAnalyzer.emoteSpread(self.commentData)
        return
    def emoteOverTime(self, emoteName, external=False, timeSegments=None, suggestions=None):
        self.commentAnalyzer.emotePopularity(self.currentVideo, self.commentData, emoteName, external, timeSegments, suggestions)
        return