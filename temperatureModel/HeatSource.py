# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 09:54:40 2022

@author: eyu
"""
from temperatureModel.HeatingItem import HeatingItem
from abc import abstractmethod, ABC


class HeatSource(ABC):
    @abstractmethod
    def moveHeat(self):
        pass
    
class HeatScript(ABC):
    @abstractmethod
    def update(self, dt):
        pass
    
    @abstractmethod
    def getHeatAfterUpdate(self):
        pass
    
    
class ConductionHeatSource(HeatSource):
    def __init__(self, heatItem1 : HeatingItem, heatItem2: HeatingItem):
        self.heatItem1 = heatItem1
        self.heatItem2 = heatItem2
        
    def setConductivity(self, conductivity):
        self.conductivity = conductivity
        
    def moveHeat(self):
        temp1 = self.heatItem1.getTemperature()
        temp2 = self.heatItem2.getTemperature()
        
        # dQ = k DT
        heatToMove12 = self.conductivity * (temp1 - temp2)
        self.heatItem1.accumulateHeat(-heatToMove12)
        self.heatItem2.accumulateHeat(heatToMove12)
        
        
class RadiationSource(HeatSource):
    def __init__(self, heatItem1 : HeatingItem, heatItem2: HeatingItem):
        self.heatItem1 = heatItem1
        self.heatItem2 = heatItem2
        
    def setScales(self, scale1, scale2):
        self.scale1 = scale1
        self.scale2 = scale2
        
    def moveHeat(self):
        temp1 = self.heatItem1.getTemperature()
        temp2 = self.heatItem2.getTemperature()
        
        # dQ a->b = e (Ta^4)
        heatToMove12 = self.scale1 * temp1**4
        heatToMove21 = self.scale2 * temp2**4
        
        self.heatItem1.accumulateHeat(heatToMove21-heatToMove12)
        self.heatItem2.accumulateHeat(heatToMove12-heatToMove21)
        
class PowerSource(HeatSource):
    def __init__(self, heatItem : HeatingItem, heatScript : HeatScript):
        self.heatItem = heatItem
        self.heatScript = heatScript
        
    def setHeatScript(self, heatScript : HeatScript):
        self.heatScript = heatScript
        
    def moveHeat(self):
        heatToAdd = self.heatScript.getHeatAfterUpdate()
        self.heatItem.accumulateHeat(heatToAdd)
        