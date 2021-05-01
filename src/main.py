from settingsUtil import SettingsUtil
from helixClient import HelixClient
import requests

settings : SettingsUtil = SettingsUtil()
currentSettings: dict = settings.getSettings()

if(not (currentSettings['client']['clientID'] and currentSettings['client']['clientSecretID'])):
    new_clientID: str = input("ClientID: ")
    new_clientSecretID: str = input("ClientSecretID: ")
    settings.setSettings(dict(clientID= new_clientID, clientSecretID= new_clientSecretID))
    currentSettings = settings.getSettings()

videoID = input("video id: ")
url = f"https://id.twitch.tv/oauth2/token"f"?client_id={currentSettings['client']['clientID']}"f"&client_secret={currentSettings['client']['clientSecretID']}"f"&grant_type=client_credentials"
bearer_token = requests.post(url).json()['access_token']

extractor : HelixClient = HelixClient(currentSettings['client']['clientID'], bearer_token)
extractor.getVideoData(videoID)
extractor.emoteAnalysis()
extractor.emoteOverTime("LUL")