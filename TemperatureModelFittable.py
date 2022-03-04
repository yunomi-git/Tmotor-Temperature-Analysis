# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 09:48:45 2022

@author: eyu
"""

from HeatSource import HeatSource, HeatScript, ConductionHeatSource, RadiationSource, PowerSource
from HeatingItem import HeatingItem
from TemperatureModel import TemperatureModel
from CurrentScript import CurrentHeatingScript
import numpy as np

class TempModelFittable(TemperatureModel):
    def __init__(self, motorConstants, parameterizedValueNames : dict, parameters=None):
        super().__init__(motorConstants)
        self.coilHeatItem = HeatingItem()
        self.motorBulkHeatItem = HeatingItem()
        self.environmentHeatItem = HeatingItem()
        
        self.motorCoilConduction = ConductionHeatSource(self.coilHeatItem, self.motorBulkHeatItem)
        self.motorEnvConduction = ConductionHeatSource(self.motorBulkHeatItem, self.environmentHeatItem)
        self.currentScript = CurrentHeatingScript(self.coilHeatItem)
        self.currentPowerSource = PowerSource(self.coilHeatItem, self.currentScript)
        
        self.simulator.addHeatItem(self.coilHeatItem)
        self.simulator.addHeatItem(self.motorBulkHeatItem)
        self.simulator.addHeatItem(self.environmentHeatItem)
        self.simulator.addHeatSource(self.motorCoilConduction)
        self.simulator.addHeatSource(self.motorEnvConduction)
        self.simulator.addHeatSource(self.currentPowerSource)
        self.simulator.addScript(self.currentScript)
        
        self.setMotorConstants(motorConstants)
        
        self.parameterizedValueNames = parameterizedValueNames
        self.numParameters = len(parameterizedValueNames)
        
        if (parameters is not None):
            self.convertParametersToModel(parameters)
        
    def setParameters(self, vectorizedParameters):
        self.updateNamedParameters(vectorizedParameters, self.namedParametersAndConstants)
        self.setNamedConstantsAndParameters(self.namedParametersAndConstants)
        
    def setMotorConstants(self, motorConstants):
        self.currentScript.setAmbientTemperature(motorConstants["coilAmbientTemperature"])
        self.currentScript.setAlpha(motorConstants["currentAlpha"])
        
    
    def setInitialConditions(self, initialConditions):
        self.coilHeatItem.setInitialTemperature(initialConditions["initialTemperature"])
        self.motorBulkHeatItem.setInitialTemperature(initialConditions["initialTemperature"])
        self.environmentHeatItem.setInitialTemperature(initialConditions["initialTemperature"])
        self.environmentHeatItem.setThermalMass(1000000.)
            
        self.currentScript.setCurrentProvider(initialConditions["currentTimeProfile"])

            
    def getOutputs(self):
        return np.array([self.coilHeatItem.getTemperature()])
    
    def updateNamedParameters(self, vectorizedParameters, parameterizedValueNames, namedParametersAndConstants):
        i = 0
        for parameterName in parameterizedValueNames:
            namedParametersAndConstants[parameterName] = vectorizedParameters[i]

    
    def setNamedConstantsAndParameters(self, namedParametersAndConstants):
        self.coilHeatItem.setThermalMass(parameters[0])
        self.motorBulkHeatItem.setThermalMass(parameters[1])
        self.motorCoilConduction.setConductivity(parameters[2])
        self.motorEnvConduction.setConductivity(parameters[3])
        self.currentScript.setResistance(parameters[4])
        
    def getVectorizedParametersList(self):
        pass
        
    def getNumParameters(self):
        return self.numParameters
