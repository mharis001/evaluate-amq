import numpy as np

class Utils:
    
    def getQuotient(self,obj):
        hashCode = obj.hashCode()
        hashCode = hashCode() >> 16
        hashCode = np.abs(hashCode)
        return np.int16(hashCode)

    def getRemainder(self,obj):
        return np.int16(obj.hashCode())

    def getIndex(self,obj,size):
        return self.getQuotient(obj)%size

