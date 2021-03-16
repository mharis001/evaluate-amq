
class Slot:
    def __init__(self,remainder=None,metaData=None):
        if remainder == None:
            self._remainder = -1 
        else:
            self._remainder = remainder
            
        if metaData == None:
            self._metadata = None
        else:
            self._metadata = metaData
    
    def getRemainder(self):
        return self._remainder
            
    def getMetaData(self):
        return self._metadata
    
    def setRemainder(self,remainder):
        self._remainder = remainder
    
    def setMetaData(self,metaData):
        self._metadata = metaData
        