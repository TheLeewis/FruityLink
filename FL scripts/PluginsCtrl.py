from abc import ABC, abstractmethod

class EqualizerCtrl(ABC):
    @staticmethod
    @abstractmethod
    def channelHasEQ(selected):
        pass
    
    @staticmethod
    @abstractmethod
    def channelOpenEQ():
        pass

    @staticmethod
    @abstractmethod
    def setFrequency(selected, slotIndex, value, currentBand):
        pass
    
    @staticmethod
    @abstractmethod
    def getFrequency(selected, slotIndex, currentBand):
        pass

    @staticmethod
    @abstractmethod
    def setGain(selected, slotIndex, value, currentBand):
        pass
    
    @staticmethod
    @abstractmethod
    def getGain(selected, slotIndex, currentBand):
        pass

    @staticmethod
    @abstractmethod
    def setQualityFactor(selected, slotIndex, value, currentBand):
        pass

    @staticmethod
    @abstractmethod
    def getQualityFactor(selected, slotIndex, currentBand):
        pass

    @staticmethod
    @abstractmethod
    def setSlope(selected, slotIndex, value, currentBand):
        pass

    @staticmethod
    @abstractmethod
    def getSlope(selected, slotIndex, currentBand):
        pass

    @staticmethod
    @abstractmethod
    def toggleBand(selected, slotIndex, currentBand):
        pass
    
    @staticmethod
    @abstractmethod
    def scrollEqShapes(selected, slotIndex, currentBand):
        pass
    
    @staticmethod
    @abstractmethod
    def getCurrentBand(state, selected, slotIndex):
        pass

    @staticmethod
    @abstractmethod
    def selectNextBand(currentBand, selected, slotIndex):
        pass
    
    @staticmethod
    @abstractmethod
    def selectPrevBand(currentBand, selected, slotIndex):
        pass

class CompressorCtrl(ABC):
    @staticmethod
    @abstractmethod
    def channelHasCompressor(selected):
        pass
    
    @staticmethod
    @abstractmethod
    def channelOpenCompressor(selected, slotIndex): # TODO: check if it's possible to implement opening the GUI window
        pass

    @staticmethod
    @abstractmethod
    def setThreshold(selected, slotIndex, value):
        pass

    @staticmethod
    @abstractmethod
    def getThreshold(selected, slotIndex):
        pass

    @staticmethod
    @abstractmethod
    def setRatio(selected, slotIndex, value):
        pass

    @staticmethod
    @abstractmethod
    def getRatio(selected, slotIndex):
        pass

    @staticmethod
    @abstractmethod
    def setAttack(selected, slotIndex, value):
        pass

    @staticmethod
    @abstractmethod
    def getAttack(selected, slotIndex):
        pass

    @staticmethod
    @abstractmethod
    def setRelease(selected, slotIndex, value):
        pass

    @staticmethod
    @abstractmethod
    def getRelease(selected, slotIndex):
        pass

    @staticmethod
    @abstractmethod
    def switchCompressorStyle(selected, slotIndex):
        pass

class ReverbCtrl(ABC):
    @staticmethod
    @abstractmethod
    def channelHasReverb(selected):
        pass
    
    @staticmethod
    @abstractmethod
    def setBrightness(selected, slotIndex, value):
        pass

    @staticmethod
    @abstractmethod
    def getBrightness(selected, slotIndex):
        pass

    @staticmethod
    @abstractmethod
    def setDistance(selected, slotIndex, value):
        pass

    @staticmethod
    @abstractmethod
    def getDistance(selected, slotIndex):
        pass
    
    @staticmethod
    @abstractmethod
    def setSpace(selected, slotIndex, value):
        pass

    @staticmethod
    @abstractmethod
    def getSpace(selected, slotIndex):
        pass

    @staticmethod
    @abstractmethod
    def setDecayRate(selected, slotIndex, value):
        pass

    @staticmethod
    @abstractmethod
    def getDecayRate(selected, slotIndex):
        pass