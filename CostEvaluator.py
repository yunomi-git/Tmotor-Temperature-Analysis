# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 23:09:47 2021

@author: Evan Yu
"""
from abc import ABC, abstractmethod
from DebugMessage import DebugMessage

class CostEvaluator(ABC):
    def __init__(self):
        self.optimizerIteration = 0
        self.debugMessage = DebugMessage()
        pass
    
    @abstractmethod
    def getCost(self, value):
        pass
    
    def setOptimizerIteration(self, iteration):
        self.optimizerIteration = iteration
    
    def getDebugMessage(self):
        return self.debugMessage
    
