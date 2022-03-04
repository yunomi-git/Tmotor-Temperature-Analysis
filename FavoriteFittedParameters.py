# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 16:56:48 2022

@author: eyu
"""
from abc import ABC, abstractmethod

class SavedParameters(ABC):
    @abstractmethod
    def getNamedParameters(self):
        pass
    
    @abstractmethod
    def getVectorParameters(self):
        pass
    
class AK109BetaParameters(SavedParameters):
    def getNamedParameters(self):
        parameters = self.getVectorParameters()
        return {"coilThermalMass" : parameters[0],
                   "motorBulkThermalMass" : parameters[1],
                   "motorCoilConductivity" : parameters[2],
                   "motorEnvConductivity" : parameters[3],
                   "motorResistance" : parameters[4]
                   }
    
    def getVectorParameters(self):
        return [9.24772914e+01, 3.09212708e+02, 4.09040187e+00, 1.98007910e+00, 1.70042713e-01]
    
class AK109AlphaParameters(SavedParameters):
    def getNamedParameters(self):
        parameters = self.getVectorParameters()
        return {"coilThermalMass" : parameters[0],
                   "motorBulkThermalMass" : parameters[1],
                   "motorCoilConductivity" : parameters[2],
                   "motorEnvConductivity" : parameters[3],
                   }
    
    def getVectorParameters(self):
        return [ 50.26554252, 204.84313289,   1.95460431,   0.77873133]
    
class AK109OrigParameters(SavedParameters):
    def getNamedParameters(self):
        parameters = self.getVectorParameters()
        return {"coilThermalMass" : parameters[0],
                "coilEnvConductivity" : parameters[1],
                   }
    
    def getVectorParameters(self):
        return [69.89597228,  1.13078779]
    
AK109FittedParameters = {"orig" : AK109OrigParameters(),
                         "alpha" : AK109AlphaParameters(),
                         "beta" : AK109BetaParameters()}