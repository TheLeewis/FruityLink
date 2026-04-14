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
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 6, selected, slotIndex)

    @staticmethod
    def getBrightness(selected, slotIndex):
        return plugins.getParamValue(6, selected, slotIndex)

    @staticmethod
    def setDistance(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 4, selected, slotIndex)

    @staticmethod
    def getDistance(selected, slotIndex):
        return plugins.getParamValue(4, selected, slotIndex)

    @staticmethod
    def setSpace(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 3, selected, slotIndex)

    @staticmethod
    def getSpace(selected, slotIndex):
        return plugins.getParamValue(3, selected, slotIndex)

    @staticmethod
    def setDecayRate(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 5, selected, slotIndex)

    @staticmethod
    def getDecayRate(selected, slotIndex):
        return plugins.getParamValue(5, selected, slotIndex)