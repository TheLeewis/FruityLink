import plugins
from Utils import Utils
from PluginsCtrl import EqualizerCtrl

EQ_SHAPES = [0, 0.14, 0.28, 0.42, 0.57, 0.71, 0.85, 1]
EQ_NAME = "Fruity Parametric EQ 2"

class FruityParametricEq2Ctrl(EqualizerCtrl):
    def __init__(self):
        pass
    
    @staticmethod
    def channelHasEQ(selected):
        for slotIndex in range(10):
            if plugins.isValid(selected, slotIndex) and plugins.getPluginName(selected, slotIndex) == EQ_NAME:
                return slotIndex
        return None
    
    @staticmethod
    def channelOpenEQ(selected, slotIndex): # TODO: check if it's possible to implement opening the GUI window
        pass

    @staticmethod
    def setFrequency(selected, slotIndex, value, currentBand):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), currentBand+7, selected, slotIndex)
    
    @staticmethod
    def getFrequency(selected, slotIndex, currentBand):
        return plugins.getParamValue(currentBand+7, selected, slotIndex)

    @staticmethod
    def setGain(selected, slotIndex, value, currentBand):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), currentBand, selected, slotIndex)
    
    @staticmethod
    def getGain(selected, slotIndex, currentBand):
        return plugins.getParamValue(currentBand, selected, slotIndex)

    @staticmethod
    def setQualityFactor(selected, slotIndex, value, currentBand):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), currentBand+14, selected, slotIndex)

    @staticmethod
    def getQualityFactor(selected, slotIndex, currentBand):
        return plugins.getParamValue(currentBand+14, selected, slotIndex)

    @staticmethod
    def setSlope(selected, slotIndex, value, currentBand):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), currentBand+28, selected, slotIndex)

    @staticmethod
    def getSlope(selected, slotIndex, currentBand):
        return plugins.getParamValue(currentBand+28, selected, slotIndex)

    @staticmethod
    def toggleBand(selected, slotIndex, currentBand):
        pass
    
    @staticmethod
    def scrollEqShapes(selected, slotIndex, currentBand):
        current_value = plugins.getParamValue(currentBand+21, selected, slotIndex)

        array_len = len(EQ_SHAPES)
        diff = 2
        shape_index = None

        for i in range(array_len):
            tmp_diff = abs(EQ_SHAPES[i] - current_value)
            if tmp_diff <= diff:
                diff = tmp_diff
                shape_index = i
        
        if shape_index < array_len - 1:
            plugins.setParamValue(EQ_SHAPES[shape_index+1], currentBand+21, selected, slotIndex)
        else:
            plugins.setParamValue(EQ_SHAPES[0], currentBand+21, selected, slotIndex)
    
    @staticmethod
    def getCurrentBand(state, selected, slotIndex):
        # 1. If a state is already present, use it
        if selected in state.keys():
            if slotIndex in state[selected].keys():
                return state[selected][slotIndex]

        # 2. Find the first active band
        for band in range(24):
            if plugins.getParamValue(band*12+band, selected, slotIndex) >= 0.5:
                return band

        # 3. Use the default band 0
        return 0

    @staticmethod
    def selectNextBand(currentBand, selected, slotIndex):
        # 1. A successive band is enabled
        for band in range(currentBand + 1, 24):
            if plugins.getParamValue(band*12+band, selected, slotIndex) >= 0.5:
                return band
        
        # 2. Start from initial
        for band in range(0, currentBand + 1):
            if plugins.getParamValue(band*12+band, selected, slotIndex) >= 0.5:
                return band
        
        # 3. zero as default
        return 0
    
    @staticmethod
    def selectPrevBand(currentBand, selected, slotIndex):
        # 1. A successive band is enabled
        for band in range(currentBand - 1, -1, -1):
            if plugins.getParamValue(band*12+band, selected, slotIndex) >= 0.5:
                return band
        
        # 2. Start from initial
        for band in range(23, currentBand - 1, -1):
            if plugins.getParamValue(band*12+band, selected, slotIndex) >= 0.5:
                return band
        
        # 3. zero as default
        return 0
