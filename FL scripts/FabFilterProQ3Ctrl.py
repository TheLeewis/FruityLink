import plugins

class FabFilterProQ3Ctrl:
    def __init__(self):
        pass
    
    @staticmethod
    def channelHasProQ3(selected):
        for slotIndex in range(10):
            if plugins.isValid(selected, slotIndex) and plugins.getPluginName(selected, slotIndex) == "FabFilter Pro-Q 3":
                return slotIndex
    
    @staticmethod
    def getProQ3FirstUsedBand(selected, slotIndex):
        for i in range(24):
            if plugins.getParamValue(12*i, selected, slotIndex) == 1:
                return i # i-th band is the first active one, so use it
    
    @staticmethod
    def toggleBandEnabled(bandIdx, selected, slotIndex):
        currentValue = plugins.getParamValue(bandIdx, selected, slotIndex)
        if currentValue >= 0.5:
            plugins.setParamValue(0, bandIdx, selected, slotIndex)
        elif currentValue < 0.5:
            plugins.setParamValue(1, bandIdx, selected, slotIndex)