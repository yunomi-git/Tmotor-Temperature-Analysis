# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 09:55:19 2022

@author: eyu
"""

class HeatingItem:
    # temperatures in celcius
    def __init__(self):
        self.heatToAdd = 0.
        
    def setInitialTemperature(self, temperature):
        self.temperature = temperature
        
    def setThermalMass(self, thermalMass):
        self.thermalMass = thermalMass
        
    def getTemperature(self):
        return self.temperature
    
    def accumulateHeat(self, heat):
        self.heatToAdd += heat
        
    def applyHeatAtDt(self, dt):
        self.temperature += self.heatToAdd / self.thermalMass * dt
        self.heatToAdd = 0
        

