from chat import Chat
from collections import defaultdict
import dateutil.parser
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import math
from settings import SettingsUtil

class Analyzer:
    def emoteSpread(self, data : Chat):
        emoteCount = 0
        emoteDict = defaultdict(int)
        for message in data.emoteMessages:
            emoteCount+=1
            for emote in message.emoticon.values():
                emoteDict[emote]+=1
        emoteDict = dict(sorted(emoteDict.items(), key=lambda item: item[1]))
        print(emoteDict)
        for emote in emoteDict.keys():
            print(emote, ": " + str(100*round(emoteDict[emote]/emoteCount, 2)) +"%")
        
    def emotePopularity(self, data, emoteName, external, timeSegments=50):
        timeSegmentation = (data.endTime-data.startTime)/timeSegments
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
                    emoteTimeCount[timeSegmentation * math.ceil(currDateTimeDelta.seconds / timeSegmentation.total_seconds())]+=1
                    break
        dataX = [h.total_seconds()/3600.0 for h in emoteTimeCount.keys()]
        self.plot(dataX, emoteTimeCount.values(), "Time (hrs into Stream)", "Frequency per Segment", emoteName)
    
    def plot(self, dataX, dataY, labelX, labelY, title):
        settingsPlotInstance = SettingsUtil().getSettings().get('plot', None)
        plt.plot(dataX, dataY, color=settingsPlotInstance.get('color', "black"))
        plt.xlabel(labelX)
        plt.ylabel(labelY)
        plt.title(title)
        plt.show()