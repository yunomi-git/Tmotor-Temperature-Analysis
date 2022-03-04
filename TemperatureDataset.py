# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:00:02 2022

@author: eyu
"""
from TemperatureModelFromFile import TempModelFromFile
from CurrentScript import CurrentTimeProfile

class TemperatureDataset:
    def __init__(self, filepath, initialTemperature, currentScript : CurrentTimeProfile):
        self.tempModel = TempModelFromFile(filepath)
        self.initialTemperature = initialTemperature
        self.currentScript = currentScript
    
    def getTemperatureModel(self):
       return self.tempModel
   
    def getInitialConditions(self):
        return {"initialTemperature" : self.initialTemperature,
                "currentTimeProfile" : self.currentScript}
   
class Run1CurrentTimeProfile(CurrentTimeProfile):
    def getCurrentAtTime(self, time): #sent 14, meas 16.37
        if (time < 40.):
            return 16.37
        else:
            return 0
        
class Run2CurrentTimeProfile(CurrentTimeProfile):
    def getCurrentAtTime(self, time): #sent 10, meas 13.7
        if (time < 60.):
            return 11.7
        else:
            return 0
        
class Run3CurrentTimeProfile(CurrentTimeProfile):
    def getCurrentAtTime(self, time): #sent 12, meas 14
        if (time < 40.):
            return 14.
        elif (time >= 40 and time < 80):
            return 0
        elif (time >= 80 and time < 120):
            return 14.
        else:
            return 0
   
run1Data = TemperatureDataset(filepath = './data/run1Data.csv',
                              initialTemperature = 22.8,
                              currentScript = Run1CurrentTimeProfile())

run2Data = TemperatureDataset(filepath = './data/run2Data.csv',
                              initialTemperature = 21.3,
                              currentScript = Run2CurrentTimeProfile())

run3Data = TemperatureDataset(filepath = './data/run3Data.csv',
                              initialTemperature = 21.3,
                              currentScript = Run3CurrentTimeProfile())

ak109Dataset = [run1Data, run2Data, run3Data]
