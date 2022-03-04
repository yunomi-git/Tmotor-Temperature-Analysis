# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 09:09:29 2022

@author: eyu
"""


from abc import ABC, abstractmethod
import numpy as np
from HeatSource import HeatSource, HeatScript
from HeatingItem import HeatingItem


class TemperatureModel(ABC):
    def __init__(self, motorConstants, parameters=None):
        self.simulator = Simulator()
    
    def getTemperaturePlot(self, initialConditions, dt, maxTime):
        time = 0.
        self.simulator.reset()
        self.setInitialConditions(initialConditions)
        
        times = np.array([time])
        outputs = np.array(self.getOutputs())
        while (time < maxTime):
            time += dt
            self.simulator.stepByDt(dt)
            
            times = np.append(times, time)
            outputs = np.append(outputs, self.getOutputs())
        
        return (times, outputs)
    
    @abstractmethod
    def setParameters(self, parameters):
        pass
    
    @abstractmethod
    def getNumParameters(self):
        pass
    
    @abstractmethod
    def setMotorConstants(self, motorConstants):
        pass
    
    @abstractmethod
    def setInitialConditions(self, initialConditions):
        pass
    
    @abstractmethod
    def getOutputs(self):
        pass
        
    
class Simulator:
    def __init__(self):
        self.heatItems = []
        self.heatSources = []
        self.scripts = []
        self.time = 0
        
    def addHeatItem(self, heatItem : HeatingItem):
        self.heatItems.append(heatItem)
        
    def addHeatSource(self, heatSource : HeatSource):
        self.heatSources.append(heatSource)
        
    def addScript(self, script : HeatScript):
        self.scripts.append(script)
        
    def stepByDt(self, dt):
        for script in self.scripts:
            script.update(self.time)
        for heatSource in self.heatSources:
            heatSource.moveHeat()
        for heatItem in self.heatItems:
            heatItem.applyHeatAtDt(dt)
            
        self.time += dt
            
    def reset(self):
        self.time = 0

        

    
    

        
        