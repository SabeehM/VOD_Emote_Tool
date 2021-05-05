import json

class SettingsUtil:
    def __init__(self) -> None:
        self.settings : dict = dict()
        self.loadSettings()

    def loadSettings(self, path: str = "./config.json") -> None:
        with open(path, encoding='utf-8') as f:
            self.settings = json.load(f)
        return

    def setSettings(self, incomingSettings:dict, path: str = "./config.json") -> None:
        with open(path, "r", encoding='utf-8') as f:
            data = json.load(f)

        for key, value in incomingSettings.items():
                data["client"][key] = value

        with open(path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
        self.loadSettings()
        return

    def getSettings(self) -> dict():
        return self.settings
