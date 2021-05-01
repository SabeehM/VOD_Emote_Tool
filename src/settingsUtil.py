import json

class SettingsUtil:
    def __init__(self):
        self.settings : dict = dict()
        self.loadSettings()

    def loadSettings(self, path: str = "./config.json"):
        with open(path) as f:
            self.settings = json.load(f)

    def setSettings(self, incomingSettings:dict, path: str = "./config.json"):
        with open(path, "r") as f:
            data = json.load(f)

        for key, value in incomingSettings.items():
                data[key] = value
                print(data[key])

        with open(path, "w") as f:
            json.dump(data, f, indent=4)
            
        self.loadSettings()
    
    def getSettings(self):
        return self.settings

