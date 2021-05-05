from .settings import SettingsUtil
from .helixClient import HelixClient
from .parameters import Parameters
from .logger import Logger
import requests, argparse


__name__ = "VODet"
__all__ = [SettingsUtil, HelixClient, Parameters, Logger]
def main() -> None:
    settings : SettingsUtil = SettingsUtil()
    currentSettings: dict = settings.getSettings()

    if(not (currentSettings['client']['clientID'] and currentSettings['client']['clientSecretID'])):
        new_clientID: str = input("ClientID: ")
        new_clientSecretID: str = input("ClientSecretID: ")
        settings.setSettings(dict(clientID= new_clientID, clientSecretID= new_clientSecretID))
        currentSettings = settings.getSettings()

    url : str = f"https://id.twitch.tv/oauth2/token"f"?client_id={currentSettings['client']['clientID']}"f"&client_secret={currentSettings['client']['clientSecretID']}"f"&grant_type=client_credentials"
    bearer_token : str = requests.post(url).json()['access_token']

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", dest="videoID", help="VideoID of the desired VOD", type=int)
    parser.add_argument("--e", dest="emotePopularity", help="Use flag to determine emotePopularity -Does not include external emotes", action="store_true")
    parser.add_argument("--t", dest="emoteName", help="Name of emote for time graph", type=str)
    parser.add_argument("--external", dest="emoteTimeExternal", help="Use flag if using time graph for external emote", action="store_true")
    parser.add_argument("--segment", dest="timeSegments", help="Seconds per segment to group emote usage in seconds. -Default is 30", type=int)
    parser.add_argument("--timestamps", dest="timestamps", help="Use flag if using timestamp recommendations. Input ax number of suggested timestamps. -Default is 3", const=-1 ,type=int, nargs="?", action="store")
    
    params = Parameters(vars(parser.parse_args()))
    
    if(not params.isValid()):
        Logger.print_fail("No action specified... -h for help")
        return
        
    extractor : HelixClient = HelixClient(currentSettings['client']['clientID'], bearer_token)

    extractor.getVideoData(params.videoID)
    
    if(params.commonSearchReq()):
        extractor.getCommentData()
    if(params.isExternal):
        extractor.searchExternalEmote(params.emoteName)
    if(params.emotePopularityProcess):
        extractor.emoteAnalysis()
    if(params.emoteName):
        extractor.emoteOverTime(params.emoteName, params.isExternal, params.timeSegments, params.numberOfTimeStamps)
    return