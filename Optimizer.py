# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 22:11:22 2021

@author: Evan Yu
"""
import numpy as np;
from abc import ABC, abstractmethod
from dataclasses import dataclass
import CostEvaluator
from DebugMessage import DebugMessage


class Optimizer(ABC):
    def __init__(self, initialValue, costEvaluator):
        self.value = initialValue;
        self.costEvaluator = costEvaluator;

        self.stepCount = 0;
        self.valueHistory = np.array([initialValue])
        self.costHistory = np.array([costEvaluator.getCost(initialValue)])
        
        self.numFeatures = initialValue.size
        
        self.maxSteps = 1
        self.printEveryNSteps = 20
        self.convergenceThreshold = 0.0

        self.endNow = False
        
        self.debugMessage = DebugMessage()
    
    @abstractmethod
    def takeStepAndGetValueAndCost(self):
        pass
    
    def step(self):
        self.debugMessage = DebugMessage()
        self.debugMessage.appendMessage("step", self.stepCount+1)
        
        self.costEvaluator.setOptimizerIteration(self.stepCount)
        value, cost = self.takeStepAndGetValueAndCost()
        self.value = value
        
        self.debugMessage.appendMessage("cost", cost)
        
        self.valueHistory = np.append(self.valueHistory, [self.value], axis=0)
        self.costHistory = np.append(self.costHistory, cost)
        self.stepCount += 1;
        
        
    def getCurrentStateAndCost(self):
        return self.valueHistory[-1], self.costHistory[-1]
    
    def getFullHistory(self):
        return (self.valueHistory, self.costHistory)
        
    def hasReachedMinimum(self, convergenceThreshold):
        if len(self.costHistory) < 2:
            return False;
        currentCost = self.costHistory[-1];
        lastCost = self.costHistory[-2];
        return abs(lastCost - currentCost) < convergenceThreshold;
    
    def setOptimizationEndConditions(self, optimizationEndConditions):
        self.maxSteps = optimizationEndConditions.maxSteps
        self.convergenceThreshold = optimizationEndConditions.convergenceThreshold
        
    def hasReachedEndCondition(self):
        return (((self.maxSteps > 0) and (self.stepCount >= self.maxSteps)) or
                (self.hasReachedMinimum(self.convergenceThreshold)) or
                (self.endNow))
    
    def endEarly(self):
        self.endNow = True
    
    def optimizeUntilEndCondition(self, optimizationEndConditions):
        self.setOptimizationEndConditions(optimizationEndConditions)
        self.stepCount = 0;
        while (not self.hasReachedEndCondition()):

            self.step();
            if (self.stepCount % self.printEveryNSteps == 0):
                self.printDebug()

    def printDebug(self):
        print(self.debugMessage)
                
    # def stoppingConditionsHaveBeenMet(self):
    #     return self.hasReachedMinimum(convergenceThreshold) or self.stepCount >= maxCount
    
    def bindEndEarly(self, endEarly):
        self.endEarly = endEarly

@dataclass
class OptimizationEndConditions:
    maxSteps : int
    convergenceThreshold : float
    
class GradientDescentOptimizer(Optimizer):
    def __init__(self, initialValue, costEvaluator, optimizationParameters):
        super().__init__(initialValue, costEvaluator);
        self.optimizationStepSize = optimizationParameters.optimizationStepSize;
        self.gradientStepFactor = optimizationParameters.gradientStepFactor;
        self.optimizationStepSizeScaling = optimizationParameters.optimizationStepSizeScaling;
        self.scaleEveryNSteps = optimizationParameters.scaleEveryNSteps
        
    def findValueGradient(self):
        numDim = self.value.size;
        valueGradient = np.zeros(numDim);
        currentCost = self.costHistory[-1];
        #construct gradient by sampling in every direction
        for i in range(numDim):
            valueTemp = np.copy(self.value);
            valueTemp[i] += self.gradientStepFactor * self.optimizationStepSize;
            costDim = self.costEvaluator.getCost(valueTemp);
            valueGradient[i] = currentCost - costDim;
        gradientNorm = np.linalg.norm(valueGradient);
        valueGradient /= gradientNorm;
        return valueGradient;
    
    def takeStepAndGetValueAndCost(self):
        if ((self.stepCount + 1) % self.scaleEveryNSteps == 0):
            self.optimizationStepSize *= self.optimizationStepSizeScaling
            
        valueGradientDirection = self.findValueGradient()
        valueStepVector = self.optimizationStepSize * valueGradientDirection;
        value = self.value + valueStepVector
        cost = self.costEvaluator.getCost(value)
        return value, cost

       
    
    
@dataclass
class OptimizationParameters:
    optimizationStepSize : float
    gradientStepFactor : float
    optimizationStepSizeScaling : float
    scaleEveryNSteps : int
    
    
    
