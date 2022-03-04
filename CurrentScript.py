# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 10:55:19 2022

@author: eyu
"""

from abc import abstractmethod, ABC
from HeatSource import HeatSource, HeatScript, ConductionHeatSource, RadiationSource, PowerSource
from HeatingItem import HeatingItem
from TemperatureModel import TemperatureModel
    
class CurrentTimeProfile(ABC):
    @abstractmethod
    def getCurrentAtTime(self, time):
        pass

class CurrentHeatingScript(HeatScript):
    def __init__(self, coil : HeatingItem):
        self.current = 0
        self.coil = coil
        
    def setCurrentProvider(self, currentProvider : CurrentTimeProfile):
        self.currentProvider = currentProvider
        
    def setAlpha(self, alpha):
        self.alpha = alpha
        
    def setResistance(self, resistance):
        self.resistance = resistance
        
    def setAmbientTemperature(self, temperature):
        self.ambientTemperature = temperature
        
    def update(self, time):
        self.current = self.currentProvider.getCurrentAtTime(time)
    
    def getHeatAfterUpdate(self):
        return self.getHeatFromCurrent(self.current)
    
    def getHeatFromCurrent(self, current):
        return ((1. + self.alpha * (self.coil.getTemperature() - self.ambientTemperature)) 
                * self.resistance * (current)**2)