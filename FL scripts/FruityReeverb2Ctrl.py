import plugins
from Utils import Utils
from PluginsCtrl import ReverbCtrl

REV_NAME = "Fruity Reeverb 2"

class FruityReeverb2Ctrl(ReverbCtrl):
    def __init__(self):
        pass

    @staticmethod
    def channelHasReverb(selected):
        for slotIndex in range(10):
            if plugins.isValid(selected, slotIndex) and plugins.getPluginName(selected, slotIndex) == REV_NAME:
                return slotIndex
        return None
    
    @staticmethod
    def setBrightness(selected, slotIndex, value):
        pass

    @staticmethod
    def getBrightness(selected, slotIndex):
        pass

    @staticmethod
    def setDistance(selected, slotIndex, value):
        pass

    @staticmethod
    def getDistance(selected, slotIndex):
        pass

    @staticmethod
    def setSpace(selected, slotIndex, value):
        pass

    @staticmethod
    def getSpace(selected, slotIndex):
        pass

    @staticmethod
    def setDecayRate(selected, slotIndex, value):
        pass

    @staticmethod
    def getDecayRate(selected, slotIndex):
        pass