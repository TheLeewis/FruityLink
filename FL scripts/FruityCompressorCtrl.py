import plugins
from Utils import Utils
from PluginsCtrl import CompressorCtrl

COMP_NAME = "Fruity Compressor"

class FruityCompressorCtrl(CompressorCtrl):
    def __init__(self):
        pass
    
    @staticmethod
    def channelHasCompressor(selected):
        for slotIndex in range(10):
            if plugins.isValid(selected, slotIndex) and plugins.getPluginName(selected, slotIndex) == COMP_NAME:
                return slotIndex
        return None
    
    @staticmethod
    def channelOpenCompressor(selected, slotIndex): # TODO: check if it's possible to implement opening the GUI window
        pass

    @staticmethod
    def setThreshold(selected, slotIndex, value):
        pass

    @staticmethod
    def getThreshold(selected, slotIndex):
        pass

    @staticmethod
    def setRatio(selected, slotIndex, value):
        pass

    @staticmethod
    def getRatio(selected, slotIndex):
        pass

    @staticmethod
    def setAttack(selected, slotIndex, value):
        pass

    @staticmethod
    def getAttack(selected, slotIndex):
        pass

    @staticmethod
    def setRelease(selected, slotIndex, value):
        pass

    @staticmethod
    def getRelease(selected, slotIndex):
        pass

    @staticmethod
    def switchCompressorStyle(selected, slotIndex):
        pass