from twitch import Helix
from twitch.helix import Video

class HelixClient:
    def __init__(self, clientID: str, bearer_token: str):
        self.helixClient =  Helix(client_id=clientID, bearer_token=bearer_token, use_cache=True)

    def getVideoData(self, videoID: str):
        foundVideo = self.helixClient.videos([videoID])[0]
        for comment in (foundVideo.comments):
            print(comment.data)