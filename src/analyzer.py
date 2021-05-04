from chat import Chat
from collections import defaultdict
from datetime import datetime, timedelta
from matplotlib.pyplot import figure
from settings import SettingsUtil
from logger import Logger
import math
import dateutil.parser
import matplotlib.pyplot as plt

__defaultTimeSegments__ = 30
__defaultSuggestionCount__ = 5
__baseURL__ = "https://twitch.tv/videos/"
class Analyzer:
    def emoteSpread(self, data : Chat):
        emoteCount = 0
        emoteDict = defaultdict(int)
        for message in data.emoteMessages:
            emoteCount+=1
            for emote in message.emoticon.values():
                emoteDict[emote]+=1
        emoteDict = dict(sorted(emoteDict.items(), key=lambda item: item[1]))
        for emote in emoteDict.keys():
            Logger.print_bold(emote + " : " + str(100*round(emoteDict[emote]/emoteCount, 2)) +"%")
        
    def emotePopularity(self, video, data, emoteName, external, timeSegments, suggestions):
        timeSegmentation = timeSegments or __defaultTimeSegments__
        timeSegmentation = timedelta(seconds=timeSegmentation)
        emoteTimestamps: list = []
        emoteTimeCount = defaultdict(int)
        dataQuery = []
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
        dataX = [h.total_seconds()/3600.0 for h in emoteTimeCount.keys()]
        suggestionCount = suggestions if suggestions else __defaultSuggestionCount__
        if(suggestions):
            sortedEmoteTimeCount = sorted(emoteTimeCount, key=emoteTimeCount.get)
            sortedEmoteTimeCount.reverse()
            #[key for key,value in emoteTimeCount.items() if value >= avgCountPerSegment]
            for timestampNumber in range(min(suggestionCount, len(sortedEmoteTimeCount))):
                timestamp = sortedEmoteTimeCount[timestampNumber]
                seconds = timestamp.total_seconds()
                Logger.print_info(__baseURL__ + video.id + "?t=" + str(int(seconds // 3600)) + "h" + str(int((seconds % 3600)) // 60) + "m" + str(int(seconds % 60)) + "s")
        self.plot(dataX, emoteTimeCount.values(), "Time (hrs into Stream)", "Frequency per Segment", emoteName)
    
    def plot(self, dataX, dataY, labelX, labelY, title):
        settingsPlotInstance = SettingsUtil().getSettings().get('plot', None)
        plt.plot(dataX, dataY, 
            color=settingsPlotInstance.get('color', "black"),
            drawstyle=settingsPlotInstance.get('drawstyle', 'default'),
            fillstyle=settingsPlotInstance.get('fillstyle', 'full'),
            linestyle=settingsPlotInstance.get('linestyle', 'solid'),
            linewidth=float(settingsPlotInstance.get('linewidth', "1"))
        )
        plt.xlabel(labelX)
        plt.ylabel(labelY)
        plt.title(title)
        saveFileName = str(datetime.now()).replace(".","-").replace(" ", "-").replace(":", "-") + ".png"
        fig = plt.gcf()
        fig.set_size_inches(float(settingsPlotInstance.get("width")),float(settingsPlotInstance.get("height")))
        fig.savefig(
            settingsPlotInstance.get("path")+saveFileName,
            dpi=settingsPlotInstance.get("dpi"),
            #quality=settingsPlotInstance.get("quality"),
            #optimize=(settingsPlotInstance.get("optimize")=="true") Depreciated as of matplotlib 3.3
        )
        Logger.print_pass("File: " + saveFileName + " saved at: " +settingsPlotInstance.get("path"))
        