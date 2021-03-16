from BitSet import *

class MetadataBitset:   
    OCCUPIED_BIT = 0
    CONTINUATION_BIT = 1
    SHIFTED_BIT = 2
    
    def __init__(self,metaData = None):
        if metaData == None:
            self._metaData = Bitset(length=3)
        else: 
            pass
            
            
        
    