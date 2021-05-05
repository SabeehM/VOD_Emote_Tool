class Parameters:
    def __init__(self, args: dict()):
        self.videoID : int = args['videoID']
        self.emotePopularityProcess : bool = args['emotePopularity']
        self.emoteName : str = args['emoteName']
        self.isExternal : bool = args['emoteTimeExternal']
        self.timeSegments : int = args['timeSegments'] or None
        self.numberOfTimeStamps : int = (args['timestamps'])
    def isValid(self) -> None:
        return (
            self.emotePopularityProcess 
            or self.emoteName
            )
    def commonSearchReq(self) -> None:
        return (
            (self.emoteName and not self.isExternal) 
            or self.emotePopularityProcess
            )
        
