class Parameters:
    def __init__(self, args: dict()):
        self.videoID = args['videoID']
        self.emotePopularityProcess = args['emotePopularity']
        self.emoteName = args['emoteName']
        self.isExternal = args['emoteTimeExternal']
        self.timeSegments = args['timeSegments'] or None
        self.numberOfTimeStamps = (args['timestamps'])
    def isValid(self):
        return (
            self.emotePopularityProcess 
            or self.emoteName
            )
    def commonSearchReq(self):
        return (
            (self.emoteName and not self.isExternal) 
            or self.emotePopularityProcess
            )
        
