# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:34:02 2022

@author: eyu
"""

from CostEvaluator import CostEvaluator
from TemperatureModelFromFile import TempModelFromFile
from TemperatureModel import TemperatureModel
from TemperatureDataset import TemperatureDataset
import numpy as np

class TimePlotCostEvaluator(CostEvaluator):
    def __init__(self, dataset : TemperatureDataset, temperatureModel : TemperatureModel):
        super().__init__()
        groundTruthModel = dataset.getTemperatureModel()
        self.initialConditions = dataset.getInitialConditions()
        self.groundTimes, self.groundTemps = groundTruthModel.getTemperaturePlot()
        self.dt = self.groundTimes[1] - self.groundTimes[0]
        self.maxTime = self.groundTimes[-1]
        
        self.temperatureModel = temperatureModel
        
    def getCost(self, value):
        self.temperatureModel.setParameters(value)
        
        # print(self.temperatureModel.coilHeatItem.temperature)
        times, outputs = self.temperatureModel.getTemperaturePlot(self.initialConditions, self.dt, self.maxTime)
        # print(self.temperatureModel.coilHeatItem.temperature)
        
        return self.getCostBetweenPlots(times, self.groundTemps, outputs)
    
    def getCostBetweenPlots(self, times, plot1, plot2):
        numPoints = times.size
        error = plot1 - plot2
        squareError = error * error
        mse = np.sum(squareError) * 1.0 / numPoints
        return mse
        
class BatchTimePlotCostEvaluator(CostEvaluator):
    def __init__(self, datasets, temperatureModel : TemperatureModel):
        super().__init__()
        self.numDatasets = len(datasets)

        self.costEvaluators = []
        for dataset in datasets:
            self.costEvaluators.append(TimePlotCostEvaluator(dataset, temperatureModel))
    
    def getCost(self, value):
        runningCost = 0
        for costEvaluator in self.costEvaluators:
            runningCost += costEvaluator.getCost(value)
            
        return runningCost / self.numDatasets