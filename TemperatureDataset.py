# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 12:00:02 2022

@author: eyu
"""
from TemperatureModelFromFile import TempModelFromFile
from CurrentScript import CurrentTimeProfile


class TemperatureDataset:
    def __init__(self, filepath, initialTemperature, ambientTemperature, currentScript : CurrentTimeProfile):
        self.tempModel = TempModelFromFile(filepath)
        self.initialTemperature = initialTemperature
        self.ambientTemperature = ambientTemperature
        self.currentScript = currentScript
    
    def getTemperatureModel(self):
       return self.tempModel
   
    def getInitialConditions(self):
        return {"initialTemperature" : self.initialTemperature,
                "ambientTemperature" : self.ambientTemperature,
                "currentTimeProfile" : self.currentScript}
    

   
# ============================================================================
class AK109Run1CurrentTimeProfile(CurrentTimeProfile):
    def getCurrentAtTime(self, time): #sent 14, meas 16.37
        if (time < 40.):
            return 16.37
        else:
            return 0
        
class AK109Run2CurrentTimeProfile(CurrentTimeProfile):
    def getCurrentAtTime(self, time): #sent 10, meas 13.7
        if (time < 60.):
            return 11.7
        else:
            return 0
        
class AK109Run3CurrentTimeProfile(CurrentTimeProfile):
    def getCurrentAtTime(self, time): #sent 12, meas 14
        if (time < 40.):
            return 14.
        elif (time >= 40 and time < 80):
            return 0
        elif (time >= 80 and time < 120):
            return 14.
        else:
            return 0
        
class AK109Run4CurrentTimeProfile(CurrentTimeProfile):
    def getCurrentAtTime(self, time): #sent 12, meas 14
        if (time < 90.):
            return 16.37
        elif (time >= 90 and time < 180):
            return 0
        elif (time >= 180 and time < 270):
            return 14.
        elif (time >= 270 and time < 360):
            return 0.
        elif (time >= 360 and time < 450):
            return 11.7
        else:
            return 0
   
ak109Run1Data = TemperatureDataset(filepath = './data/ak109Run1Data.csv',
                              initialTemperature = 22.8,
                              ambientTemperature = 22.8,
                              currentScript = AK109Run1CurrentTimeProfile())

ak109Run2Data = TemperatureDataset(filepath = './data/ak109Run2Data.csv',
                              initialTemperature = 21.3,
                              ambientTemperature = 21.3,
                              currentScript = AK109Run2CurrentTimeProfile())

ak109Run3Data = TemperatureDataset(filepath = './data/ak109Run3Data.csv',
                              initialTemperature = 21.3,
                              ambientTemperature = 21.3,
                              currentScript = AK109Run3CurrentTimeProfile())

ak109Run4Data = TemperatureDataset(filepath = './data/ak109Run4Data.csv',
                              initialTemperature = 21.4,
                              ambientTemperature = 21.4,
                              currentScript = AK109Run4CurrentTimeProfile())

ak109Dataset = [ak109Run1Data, ak109Run2Data, ak109Run3Data, ak109Run4Data]

# ============================================================================
class AK809CurrentTimeProfile(CurrentTimeProfile):
    def getCurrentAtTime(self, time): #sent 12, meas 14
        if (time < 60.):
            return 9.75
        elif (time >= 60 and time < 150):
            return 0
        elif (time >= 150 and time < 270):
            return 8.52
        elif (time >= 270 and time < 360):
            return 0.
        elif (time >= 360 and time < 450):
            return 7.31
        else:
            return 0
        
ak809Run1Data = TemperatureDataset(filepath = './data/ak809Run1Data.csv',
                              initialTemperature = 21.0,
                              ambientTemperature = 21.4,
                              currentScript = AK809CurrentTimeProfile())

ak809Dataset = [ak809Run1Data]

# ============================================================================
class AK606Run1CurrentTimeProfile(CurrentTimeProfile):
    def getCurrentAtTime(self, time): #sent 12, meas 14
        if (time < 90.):
            return 3.6
        elif (time >= 90 and time < 180):
            return 0
        elif (time >= 180 and time < 270):
            return 2.95
        elif (time >= 270 and time < 360):
            return 0.
        elif (time >= 360 and time < 450):
            return 2.0
        else:
            return 0
        
class AK606Run2CurrentTimeProfile(CurrentTimeProfile):
    def getCurrentAtTime(self, time): #sent 12, meas 14
        if (time < 90.):
            return 4.4
        elif (time >= 90 and time < 180):
            return 0
        elif (time >= 180 and time < 270):
            return 2.95
        elif (time >= 270 and time < 360):
            return 0.
        elif (time >= 360 and time < 450):
            return 3.6
        else:
            return 0
        
ak606Run1Data = TemperatureDataset(filepath = './data/ak606Run1Data.csv',
                              initialTemperature = 21.3,
                              ambientTemperature = 20.4,
                              currentScript = AK606Run1CurrentTimeProfile())

ak606Run2Data = TemperatureDataset(filepath = './data/ak606Run2Data.csv',
                              initialTemperature = 22.4,
                              ambientTemperature = 20.6,
                              currentScript = AK606Run2CurrentTimeProfile())

ak606Dataset = [ak606Run1Data, ak606Run2Data]

allDatasets = {"AK606" : ak606Dataset,
               "AK809" : ak809Dataset,
               "AK109" : ak109Dataset}


