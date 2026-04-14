import plugins
from Utils import Utils
from PluginsCtrl import CompressorCtrl

COMP_NAME = "Fruity Compressor"
COMPRESSOR_STYLES = [0, 0.14, 0.28, 0.42, 0.57, 0.71, 0.85, 1]

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
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 0, selected, slotIndex)

    @staticmethod
    def getThreshold(selected, slotIndex):
        return plugins.getParamValue(0, selected, slotIndex)

    @staticmethod
    def setRatio(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 1, selected, slotIndex)

    @staticmethod
    def getRatio(selected, slotIndex):
        return plugins.getParamValue(1, selected, slotIndex)

    @staticmethod
    def setAttack(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 3, selected, slotIndex)

    @staticmethod
    def getAttack(selected, slotIndex):
        return plugins.getParamValue(3, selected, slotIndex)

    @staticmethod
    def setRelease(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 4, selected, slotIndex)

    @staticmethod
    def getRelease(selected, slotIndex):
        return plugins.getParamValue(4, selected, slotIndex)

    @staticmethod
    def switchCompressorStyle(selected, slotIndex):
        current_value = plugins.getParamValue(0, selected, slotIndex)
        
        array_len = len(COMPRESSOR_STYLES)
        diff = 2
        style_index = None

        for i in range(array_len):
            tmp_diff = COMPRESSOR_STYLES[i] - current_value
            if abs(tmp_diff) < diff:
                diff = tmp_diff
                style_index = i
        
        if style_index < array_len - 1:
            return COMPRESSOR_STYLES[style_index+1]
        else:
            return COMPRESSOR_STYLES[0]