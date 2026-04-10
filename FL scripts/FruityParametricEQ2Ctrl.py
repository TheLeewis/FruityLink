import plugins
from Utils import Utils
from PluginsCtrl import EqualizerCtrl

EQ_SHAPES = []
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
        pass
    
    @staticmethod
    def getFrequency(selected, slotIndex, currentBand):
        pass

    @staticmethod
    def setGain(selected, slotIndex, value, currentBand):
        pass
    
    @staticmethod
    def getGain(selected, slotIndex, currentBand):
        pass

    @staticmethod
    def setQualityFactor(selected, slotIndex, value, currentBand):
        pass

    @staticmethod
    def getQualityFactor(selected, slotIndex, currentBand):
        pass

    @staticmethod
    def setSlope(selected, slotIndex, value, currentBand):
        pass

    @staticmethod
    def getSlope(selected, slotIndex, currentBand):
        pass

    @staticmethod
    def toggleBand(selected, slotIndex, currentBand):
        pass
    
    @staticmethod
    def scrollEqShapes(selected, slotIndex, currentBand):
        pass
    
    @staticmethod
    def getCurrentBand(state, selected, slotIndex):
        pass

    @staticmethod
    def selectNextBand(currentBand, selected, slotIndex):
        pass
    
    @staticmethod
    def selectPrevBand(currentBand, selected, slotIndex):
        pass
