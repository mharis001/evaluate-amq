import numpy as np
from Slot import *
from Utils import *


class QuotientFilter:
    DEFAULT_SIZE = 1000
    
    def __init__(self,size = 0):
        self._qfSize = 0
        if size == 0:
            self._set = np.zeros(self.DEFAULT_SIZE)
            for i in range(1000):
                self._set[i] = Slot()
            self._capacity =  self.DEFAULT_SIZE
        else:
            self._set = np.zeros(size)
            for i in range(1000):
                self._set[i] = Slot()
            self._capacity =  size   
                        
    def getCapacity(self):
        return self._capacity
    
    def getSize(self):
        return self._qfSize
    
    def isFull(self):
        return self.getSize() >= self.getCapacity()
    
    def setSlot(self,index, slot):
        self._set[index] = slot
    
    def getSet(self):
        return self._set
    
    def insert(self,obj):
        if self.isFull():
            raise IOError("ERROR: Quotient Filter has reached capacity")
        
        index = Utils().getIndex(obj,self.getCapacity())
        currentSlot = self._set[index]
        remainder = Utils().getRemainder(obj)
            
    
    # def insert(self):
    #     pass
    
    # def mayContain(self):
    #     pass
    
    # def remove(self):
    #     pass
    
    # def merge(self):
    #     pass
    
    # def clear(self):
    #     pass
    
    # def getTableSize(self):
    #     pass
    
    # def startIterator(self):
    #     pass
    
    # def finishIterator(self):
    #     pass
    
    # def next(self):
    #     pass
    
    
'''
Methods to implement
1. qf_init
Descrption: 
- Initializes a quotient filter with capacity 2^q.
- Increasing r improves the filter's accuracy but uses more space. 
- Returns false if q == 0, r == 0, q+r > 64, or on ENOMEM.

2. qf_may_contain

'''