import plugins
from Utils import Utils

EQ_SHAPES = [0.0, 0.125, 0.250, 0.375, 0.5, 0.625, 0.750, 0.875, 1.0]

class FabFilterProQ3Ctrl:
    def __init__(self):
        pass
    
    @staticmethod
    def channelHasProQ3(selected):
        for slotIndex in range(10):
            if plugins.isValid(selected, slotIndex) and plugins.getPluginName(selected, slotIndex) == "FabFilter Pro-Q 3":
                return slotIndex
        return None
    
    @staticmethod
    def channelOpenProQ3(selected, slotIndex): # TODO: check if it's possible to implement opening the GUI window
        pass

    @staticmethod
    def setFrequency(selected, slotIndex, value, currentBand):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 2+currentBand*12+currentBand, selected, slotIndex)
    
    @staticmethod
    def getFrequency(selected, slotIndex, currentBand):
        return plugins.getParamValue(2+currentBand*12+currentBand, selected, slotIndex)

    @staticmethod
    def setGain(selected, slotIndex, value, currentBand):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 3+currentBand*12+currentBand, selected, slotIndex)
    
    @staticmethod
    def getGain(selected, slotIndex, currentBand):
        return plugins.getParamValue(3+currentBand*12+currentBand, selected, slotIndex)

    @staticmethod
    def setQualityFactor(selected, slotIndex, value, currentBand):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 7+currentBand*12+currentBand, selected, slotIndex)

    @staticmethod
    def getQualityFactor(selected, slotIndex, currentBand):
        return plugins.getParamValue(7+currentBand*12+currentBand, selected, slotIndex)

    @staticmethod
    def setSlope(selected, slotIndex, value, currentBand):
        plugins.setParamValue(Utils.mapMidiCCTo01(value), 9+currentBand*12+currentBand, selected, slotIndex)

    @staticmethod
    def getSlope(selected, slotIndex, currentBand):
        return plugins.getParamValue(9+currentBand*12+currentBand, selected, slotIndex)

    @staticmethod
    def toggleBand(selected, slotIndex, currentBand):
        current_value = plugins.getParamValue(1+currentBand*12+currentBand, selected, slotIndex)
        
        if current_value < 0.5:
            toSet = 1
        elif current_value >= 0.5:
            toSet = 0
        
        plugins.setParamValue(toSet, 1+currentBand*12+currentBand, selected, slotIndex)
    
    @staticmethod
    def scrollEqShapes(selected, slotIndex, currentBand):
        current_value = plugins.getParamValue(8+currentBand*12+currentBand, selected, slotIndex)

        array_len = len(EQ_SHAPES)
        diff = 2
        shape_index = None

        for i in range(array_len):
            tmp_diff = abs(EQ_SHAPES[i] - current_value)
            if tmp_diff <= diff:
                diff = tmp_diff
                shape_index = i
        
        if shape_index < array_len - 1:
            plugins.setParamValue(EQ_SHAPES[shape_index+1], 8+currentBand*12+currentBand, selected, slotIndex)
        else:
            plugins.setParamValue(EQ_SHAPES[0], 8+currentBand*12+currentBand, selected, slotIndex)
    
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
