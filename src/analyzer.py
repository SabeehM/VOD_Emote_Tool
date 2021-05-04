from chat import Chat
from collections import defaultdict
from datetime import datetime, timedelta
from matplotlib.pyplot import figure
from settings import SettingsUtil
from logger import Logger
from twitch.helix import Video
import math
import dateutil.parser
import matplotlib.pyplot as plt

__defaultTimeSegments__ = 30
__defaultSuggestionCount__ = 3
__baseURL__ = "https://twitch.tv/videos/"

class Analyzer:
    def emoteSpread(self, data : Chat):
        emoteCount : int = 0
        emoteDict : dict() = defaultdict(int)
        for message in data.emoteMessages:
            emoteCount+=1
            for emote in message.emoticon.values():
                emoteDict[emote]+=1
        emoteDict = dict(sorted(emoteDict.items(), key=lambda item: item[1]))
        for emote in emoteDict.keys():
            Logger.print_bold(emote + " : " + str(100*round(emoteDict[emote]/emoteCount, 2)) +"%")
        
    def emotePopularity(self, video : Video, data : Chat, emoteName : str, external : bool, timeSegments : int, suggestions : int) -> None:
        timeSegmentation : int = timeSegments or __defaultTimeSegments__
        timeSegmentation : timedelta = timedelta(seconds=timeSegmentation)
        emoteTimestamps: list = []
        emoteTimeCount : defaultdict = defaultdict(int)
        dataQuery : list = []
        if(not external):
            dataQuery = data.emoteMessages
        else:
            dataQuery = data.externalEmoteMessages
        for message in dataQuery:
            for emote in message.emoticon.values():
                if(emote.lower() == emoteName.lower()):
                    currDateTimeDelta = dateutil.parser.parse(message.date)-data.startTime
                    emoteTimestamps.append(currDateTimeDelta)
                    emoteTimeCount[timeSegmentation * math.floor(currDateTimeDelta.seconds / timeSegmentation.total_seconds())]+=1
                    break
        if(not len(emoteTimeCount.keys())):
            Logger.print_warn("No emotes found...")
            return
        dataX : list = [h.total_seconds()/3600.0 for h in emoteTimeCount.keys()]
        suggestionCount : int = suggestions if (suggestions!=-1) else __defaultSuggestionCount__
        if(suggestions):
            sortedEmoteTimeCount : list = sorted(emoteTimeCount, key=emoteTimeCount.get)
            sortedEmoteTimeCount.reverse()
            for timestampNumber in range(min(suggestionCount, len(sortedEmoteTimeCount))):
                timestamp = sortedEmoteTimeCount[timestampNumber]
                seconds = timestamp.total_seconds()
                Logger.print_info(__baseURL__ + video.id + "?t=" + str(int(seconds // 3600)) + "h" + str(int((seconds % 3600)) // 60) + "m" + str(int(seconds % 60)) + "s")
        self.plot(dataX, emoteTimeCount.values(), "Time (hrs into Stream)", "Frequency per Segment", data.streamer + " : " + emoteName)
        return

    def plot(self, dataX : list, dataY : list, labelX : str, labelY : str, title : str):
        settingsPlotInstance = SettingsUtil().getSettings().get('plot', None)
        plt.plot(dataX, dataY, 
            color=settingsPlotInstance.get('styles').get('color', "black"),
            drawstyle=settingsPlotInstance.get('styles').get('drawstyle', 'default'),
            fillstyle=settingsPlotInstance.get('styles').get('fillstyle', 'full'),
            linestyle=settingsPlotInstance.get('styles').get('linestyle', 'solid'),
            linewidth=float(settingsPlotInstance.get('styles').get('linewidth', "1"))
        )
        plt.xlabel(labelX)
        plt.ylabel(labelY)
        plt.title(title)
        saveFileName = str(datetime.now()).replace(".","-").replace(" ", "-").replace(":", "-") + ".png"
        fig = plt.gcf()
        fig.set_size_inches(float(settingsPlotInstance.get('properties').get("width")),float(settingsPlotInstance.get('properties').get("height")))
        fig.savefig(
            settingsPlotInstance.get("path")+saveFileName,
            dpi=settingsPlotInstance.get('properties').get("dpi"),
            #quality=settingsPlotInstance.get('properties').get("quality"),
            #optimize=(settingsPlotInstance.get('properties').get("optimize")=="true") Depreciated as of matplotlib 3.3
        )
        Logger.print_pass("File: " + saveFileName + " saved at: " +settingsPlotInstance.get("path"))
        