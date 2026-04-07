import json
import os
import sys

class Persistence:
    def __init__(self):
        pass
    
    @staticmethod
    def getFilePath(filename="memory.json"):
        # Check if the script is running as a bundled executable
        if getattr(sys, 'frozen', False):
            # Path where the .exe is located
            base_path = os.path.dirname(sys.executable)
        else:
            # Path where the .py script is located
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(base_path, filename)
    
    @staticmethod
    def saveSettings(ipc1, ipc2, ipc3, ipc4, flIn, flOut, midasIn, midasOut):
        path = Persistence.getFilePath()

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

        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)