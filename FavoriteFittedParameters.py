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
        return [8.00757115e+01, 3.12048115e+02, 3.77217667e+00, 9.90026858e-01, 1.38781825e-01]
    
class AK109AlphaParameters(SavedParameters):
    def getNamedParameters(self):
        parameters = self.getVectorParameters()
        return {"coilThermalMass" : parameters[0],
                   "motorBulkThermalMass" : parameters[1],
                   "motorCoilConductivity" : parameters[2],
                   "motorEnvConductivity" : parameters[3],
                   }
    
    def getVectorParameters(self):
        return [5.34969505e+01, 2.27947001e+02, 2.35468820e+00, 2.27722436e-01]
    
class AK109OrigParameters(SavedParameters):
    def getNamedParameters(self):
        parameters = self.getVectorParameters()
        return {"coilThermalMass" : parameters[0],
                "coilEnvConductivity" : parameters[1],
                   }
    
    def getVectorParameters(self):
        return [76.30648511, 1.0942789]
    
AK109FittedParameters = {"orig" : AK109OrigParameters(),
                         "alpha" : AK109AlphaParameters(),
                         "beta" : AK109BetaParameters()}