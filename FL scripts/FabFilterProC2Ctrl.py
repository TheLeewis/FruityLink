import plugins
from Utils import Utils

COMPRESSOR_STYLES = [0, 0.12, 0.28, 0.42, 0.57, 0.71, 0.85, 1]
'''
CLEAN = 0
CLASSIC = 0.14
OPTO = 0.28
VOCAL = 0.42
MASTERING = 0.57
BUS = 0.71
PUNCH = 0.85
PUMPING = 1
'''

class FabFilterProC2Ctrl:
    def __init__(self):
        pass
    
    @staticmethod
    def channelHasProC2(selected):
        for slotIndex in range(10):
            if plugins.isValid(selected, slotIndex) and plugins.getPluginName(selected, slotIndex) == "FabFilter Pro-C 2":
                return slotIndex
        return None
    
    @staticmethod
    def channelOpenProC2(selected, slotIndex): # TODO: check if it's possible to implement opening the GUI window
        pass

    @staticmethod
    def setThreshold(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 1, selected, slotIndex)

    @staticmethod
    def getThreshold(selected, slotIndex):
        return plugins.getParamValue(1, selected, slotIndex)

    @staticmethod
    def setRatio(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 2, selected, slotIndex)

    @staticmethod
    def getRatio(selected, slotIndex):
        return plugins.getParamValue(2, selected, slotIndex)

    @staticmethod
    def setAttack(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 5, selected, slotIndex)

    @staticmethod
    def getAttack(selected, slotIndex):
        return plugins.getParamValue(5, selected, slotIndex)

    @staticmethod
    def setRelease(selected, slotIndex, value):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 6, selected, slotIndex)

    @staticmethod
    def getRelease(selected, slotIndex):
        return plugins.getParamValue(6, selected, slotIndex)

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