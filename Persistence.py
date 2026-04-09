import json
import os
import sys

class Persistence:
    def __init__(self):
        pass
    
    @staticmethod
    def getFilePath(filename="preferences.json"):
        try:
            appDataPath = os.getenv('LOCALAPPDATA')
            basePath = os.path.join(appDataPath, 'FruityLink')

            os.makedirs(basePath, exist_ok=True)
            
            return os.path.join(basePath, filename)
        except:
            return None
    
    @staticmethod
    def saveSettings(ipc1, ipc2, ipc3, ipc4, flIn, flOut, midasIn, midasOut):
        path = Persistence.getFilePath()

        if path is not None:
            data = {
                "ipc1": ipc1,
                "ipc2": ipc2,
                "ipc3": ipc3,
                "ipc4": ipc4,
                "flIn": flIn,
                "flOut": flOut,
                "midasIn": midasIn,
                "midasOut": midasOut
            }

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

    @staticmethod
    def getSettings():
        path = Persistence.getFilePath()

        if path is not None and os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return None