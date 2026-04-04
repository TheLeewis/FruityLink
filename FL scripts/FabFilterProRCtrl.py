import plugins
import Utils

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
        plugins.setParamValue(Utils.mapMidiCCTo01(value), "Brightness", selected, slotIndex)

    @staticmethod
    def setDistance(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), "Distance", selected, slotIndex)

    @staticmethod
    def setSpace(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), "Space", selected, slotIndex)

    @staticmethod
    def setDecayRate(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), "Decay Rate", selected, slotIndex)