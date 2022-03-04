# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 10:18:44 2022

@author: eyu
"""
from HeatSource import HeatSource, HeatScript, ConductionHeatSource, RadiationSource, PowerSource
from HeatingItem import HeatingItem
from TemperatureModel import TemperatureModel
from CurrentScript import CurrentHeatingScript
import numpy as np

        
# This model only accounts for conduction.
# A coil is connected to the motor, which is connected to the environment
class TempModelAlpha(TemperatureModel):
    def __init__(self, motorConstants, parameters=None):
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
        
        if (parameters is not None):
            self.convertParametersToModel(parameters)
        
    def setParameters(self, parameters):
        self.convertParametersToModel(parameters)
        
    def setMotorConstants(self, motorConstants):
        self.currentScript.setAmbientTemperature(motorConstants["coilAmbientTemperature"])
        self.currentScript.setAlpha(motorConstants["currentAlpha"])
        self.currentScript.setResistance(motorConstants["motorResistance"])
    
    def setInitialConditions(self, initialConditions):
        self.coilHeatItem.setInitialTemperature(initialConditions["initialTemperature"])
        self.motorBulkHeatItem.setInitialTemperature(initialConditions["initialTemperature"])
        self.environmentHeatItem.setInitialTemperature(initialConditions["initialTemperature"])
        self.environmentHeatItem.setThermalMass(1000000.)
            
        self.currentScript.setCurrentProvider(initialConditions["currentTimeProfile"])

            
    def getOutputs(self):
        return np.array([self.coilHeatItem.getTemperature()])
    
    def convertParametersToModel(self, parameters):
        self.coilHeatItem.setThermalMass(parameters[0])
        self.motorBulkHeatItem.setThermalMass(parameters[1])
        self.motorCoilConduction.setConductivity(parameters[2])
        self.motorEnvConduction.setConductivity(parameters[3])
        
    def getNumParameters(self):
        return 4
    
class TempModelOrig(TemperatureModel):
    def __init__(self, motorConstants, parameters=None):
        super().__init__(motorConstants)
        self.coilHeatItem = HeatingItem()
        self.environmentHeatItem = HeatingItem()
        
        self.coilEnvConduction = ConductionHeatSource(self.coilHeatItem, self.environmentHeatItem)
        self.currentScript = CurrentHeatingScript(self.coilHeatItem)
        self.currentPowerSource = PowerSource(self.coilHeatItem, self.currentScript)
        
        self.simulator.addHeatItem(self.coilHeatItem)
        self.simulator.addHeatItem(self.environmentHeatItem)
        self.simulator.addHeatSource(self.coilEnvConduction)
        self.simulator.addHeatSource(self.currentPowerSource)
        self.simulator.addScript(self.currentScript)
        
        self.setMotorConstants(motorConstants)
       
        if (parameters is not None):
            self.convertParametersToModel(parameters)
        
    def setParameters(self, parameters):
        self.convertParametersToModel(parameters)
        
    def setMotorConstants(self, motorConstants):
        self.currentScript.setAmbientTemperature(motorConstants["coilAmbientTemperature"])
        self.currentScript.setAlpha(motorConstants["currentAlpha"])
        self.currentScript.setResistance(motorConstants["motorResistance"])
    
    def setInitialConditions(self, initialConditions):
        self.coilHeatItem.setInitialTemperature(initialConditions["initialTemperature"])
        self.environmentHeatItem.setInitialTemperature(initialConditions["initialTemperature"])
        self.environmentHeatItem.setThermalMass(1000000.)
        
        self.currentScript.setCurrentProvider(initialConditions["currentTimeProfile"])
            
    def getOutputs(self):
        return np.array([self.coilHeatItem.getTemperature()])
    
    def convertParametersToModel(self, parameters):
        self.coilHeatItem.setThermalMass(parameters[0])
        self.coilEnvConduction.setConductivity(parameters[1])
        
    def getNumParameters(self):
        return 2
    
class TempModelBeta(TemperatureModel):
    def __init__(self, motorConstants, parameters=None):
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
        
        if (parameters is not None):
            self.convertParametersToModel(parameters)
        
    def setParameters(self, parameters):
        self.convertParametersToModel(parameters)
        
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
    
    def convertParametersToModel(self, parameters):
        self.coilHeatItem.setThermalMass(parameters[0])
        self.motorBulkHeatItem.setThermalMass(parameters[1])
        self.motorCoilConduction.setConductivity(parameters[2])
        self.motorEnvConduction.setConductivity(parameters[3])
        self.currentScript.setResistance(parameters[4])
        
    def getNumParameters(self):
        return 5
