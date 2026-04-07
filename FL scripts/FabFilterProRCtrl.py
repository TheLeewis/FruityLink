import plugins
from Utils import Utils

class FabFilterProRCtrl:
    def __init__(self):
        pass

    @staticmethod
    def channelHasProR(selected):
        for slotIndex in range(10):
            if plugins.isValid(selected, slotIndex) and plugins.getPluginName(selected, slotIndex) == "FabFilter Pro-R":
                return slotIndex
        return None
    
    @staticmethod
    def setBrightness(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 2, selected, slotIndex)

    @staticmethod
    def getBrightness(selected, slotIndex):
        return plugins.setParamValue(2, selected, slotIndex)

    @staticmethod
    def setDistance(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 4, selected, slotIndex)

    @staticmethod
    def getDistance(selected, slotIndex):
        return plugins.setParamValue(4, selected, slotIndex)

    @staticmethod
    def setSpace(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 0, selected, slotIndex)

    @staticmethod
    def getSpace(selected, slotIndex):
        return plugins.setParamValue(0, selected, slotIndex)

    @staticmethod
    def setDecayRate(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 1, selected, slotIndex)

    @staticmethod
    def getDecayRate(selected, slotIndex):
        return plugins.setParamValue(1, selected, slotIndex)