# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 16:56:48 2022

@author: eyu
"""
from abc import ABC, abstractmethod
import numpy as np

class SavedParameters(ABC):
    @abstractmethod
    def getNamedParametersForFit(self, fitname):
        pass
    
    def getVectorParametersForFit(self, fitname):
        return np.array(self.parameters[fitname])
    
class EveryParameterStorage():
    def __init__(self):
        self.allParameters = {}
    
    def setMotorModelParameters(self, motorName, modelName, motorModelParameters):
        if not motorName in self.allParameters.keys():
            motorParameters = {}
            self.allParameters[motorName] = motorParameters
        else:
            motorParameters = self.allParameters[motorName]
        motorParameters[modelName] = motorModelParameters
        
    
    def getParametersForMotorModelFit(self, motorName, modelName, fitName):
        motorParameters = self.allParameters[motorName]
        modelParameters = motorParameters[modelName]
        parameters = modelParameters.getVectorParametersForFit(fitName)
        return parameters
    
class AK109BetaParameters(SavedParameters):
    def __init__(self):
        self.parameters = {"fit123" : [9.24772914e+01, 3.09212708e+02, 4.09040187e+00, 1.98007910e+00, 1.70042713e-01]}
        
    def getNamedParametersForFit(self, fitname):
        parameters = self.getVectorParameters(fitname)
        return {"coilThermalMass" : parameters[0],
                   "motorBulkThermalMass" : parameters[1],
                   "motorCoilConductivity" : parameters[2],
                   "motorEnvConductivity" : parameters[3],
                   "motorResistance" : parameters[4]
                   }        
    
    
class AK109AlphaParameters(SavedParameters):
    def __init__(self):
        self.parameters = {"fit123" : [ 50.26554252, 204.84313289,   1.95460431,   0.77873133],
                           "fit4" : [ 48.39351414, 247.47682642,   1.75475715,   0.40623879],
                           'fit1234' : [ 51.00502884, 246.16215547,   1.80814198,   0.37162564]}
        
    def getNamedParametersForFit(self, fitname):
        parameters = self.getVectorParameters()
        return {"coilThermalMass" : parameters[0],
                   "motorBulkThermalMass" : parameters[1],
                   "motorCoilConductivity" : parameters[2],
                   "motorEnvConductivity" : parameters[3],
                   }
    
class AK109OrigParameters(SavedParameters):
    def __init__(self):
        self.parameters = {"fit123" : [69.89597228,  1.13078779],
                           'fit4' : [114.31770598,   0.56354714]}
        
    def getNamedParametersForFit(self, fitname):
        parameters = self.getVectorParameters(fitname)
        return {"coilThermalMass" : parameters[0],
                "coilEnvConductivity" : parameters[1],
                   }

class AK809AlphaParameters(SavedParameters):
    def __init__(self):
        self.parameters = {"fit1" : [ 40.37157793, 334.79052868,   1.77701089,   0.74043355]
                           }
        
    def getNamedParametersForFit(self, fitname):
        parameters = self.getVectorParameters()
        return {"coilThermalMass" : parameters[0],
                   "motorBulkThermalMass" : parameters[1],
                   "motorCoilConductivity" : parameters[2],
                   "motorEnvConductivity" : parameters[3],
                   }
    
class AK606AlphaParameters(SavedParameters):
    def __init__(self):
        self.parameters = {"fit1" : [3.31326089e+00, 2.47799367e+01, 1.50697775e-01, 1.96396497e-02],
                           "fit2" : [17.70070787, 18.81621937,  0.26140927,  0.02798457],
                           "manual1" : [3.20865623, 23.15129403,  0.15020281,  0.03438256],
                           "manual2" : [  16.8, 18.0, 0.212, 0.041]}
        
    def getNamedParametersForFit(self, fitname):
        parameters = self.getVectorParameters()
        return {"coilThermalMass" : parameters[0],
                   "motorBulkThermalMass" : parameters[1],
                   "motorCoilConductivity" : parameters[2],
                   "motorEnvConductivity" : parameters[3],
                   }
    

allFittedMotorParameters = EveryParameterStorage()
allFittedMotorParameters.setMotorModelParameters("AK109", "alpha", AK109AlphaParameters())
allFittedMotorParameters.setMotorModelParameters("AK109", "beta", AK109BetaParameters())
allFittedMotorParameters.setMotorModelParameters("AK109", "orig", AK109OrigParameters())
allFittedMotorParameters.setMotorModelParameters("AK809", "alpha", AK809AlphaParameters())
allFittedMotorParameters.setMotorModelParameters("AK606", "alpha", AK606AlphaParameters())
