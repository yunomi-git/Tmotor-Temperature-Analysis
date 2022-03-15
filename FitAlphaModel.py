# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:49:19 2022

@author: eyu
"""

from HeatSource import HeatSource, HeatScript, ConductionHeatSource, RadiationSource, PowerSource
from HeatingItem import HeatingItem
from TemperatureModel import TemperatureModel
from CurrentScript import CurrentHeatingScript, CurrentTimeProfile
from TemperatureModelInstances import TempModelAlpha, TempModelOrig
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
from TempModelPlotter import TempModelPlotter
from TemperatureModelFromFile import TempModelFromFile
import pyqtgraph as pg
from TimePlotCostEvaluator import TimePlotCostEvaluator, BatchTimePlotCostEvaluator
from GeneticOptimizer import SimpleGAOptimizer, SimpleGAParameters
from Optimizer import OptimizationEndConditions, GradientDescentOptimizer, GDOptimizationParameters
import time
from TemperatureDataset import allDatasets
from MotorConstants import akMotorConstants
from FavoriteFittedParameters import allFittedMotorParameters



def generateInitialParametersAround(parametersCenter, scale):
    initialParameters = np.random.rand(populationSize, numParameters) * scale - scale/2
    if parametersCenter is not None:
        initialParameters[0,:] = np.zeros(numParameters)
        initialParameters += parametersCenter
    return initialParameters

# ============================================================================
# GUI
plotEveryNSteps = 2

# ============================================================================
# Model
motorName = "AK606"
modelName = "alpha"
dataset = [allDatasets[motorName][1]]
motorConstants = akMotorConstants

temperatureModel = TempModelAlpha(motorConstants)
numParameters = temperatureModel.getNumParameters()

# Optimizer
costEvaluator = BatchTimePlotCostEvaluator(dataset, temperatureModel)

scale = 1.
populationSize = 10

seedFitName = "manual2"
seedParameters = allFittedMotorParameters.getParametersForMotorModelFit(motorName, modelName, seedFitName) 
# seedParameters += np.random.rand(4) * 3

initialParameters = generateInitialParametersAround(seedParameters, scale)

# optimizationParameters = SimpleGAParameters(crossoverRatio=0.5, 
#                                             mutationMagnitude=5.,
#                                             decreaseMutationMagnitudeEveryNSteps=50,
#                                             mutationMagnitudeLearningRate=0.9,
#                                             mutationChance=1.0,
#                                             decreaseMutationChanceEveryNSteps=200,
#                                             mutationChanceLearningRate=0.9,
#                                             mutateWithNormalDistribution=False,
#                                             mutationLargeCostScalingFactor=5.,
#                                             diversityChoiceRatio = 0.3,
#                                             varianceMutationMaxMagnitude = 5.,
#                                             weightedMutationScaling = np.array([1., 1., 0.01, 0.01]));
  
optimizationParameters = GDOptimizationParameters(optimizationStepSize = 2.,
                                                    gradientStepFactor = 0.1,
                                                    optimizationStepSizeScaling = 0.95,
                                                    scaleEveryNSteps = 1,
                                                    weightedScaling = np.array([1., 1., 0.1, 0.1]));  

optimizationEndConditions = OptimizationEndConditions(maxSteps=300,
                                                      convergenceThreshold=0.0)

printEveryNSteps = 100

# optimizer = SimpleGAOptimizer(initialParameters, costEvaluator, optimizationParameters)
optimizer = GradientDescentOptimizer(seedParameters, costEvaluator, optimizationParameters)
optimizer.printEveryNSteps = printEveryNSteps
optimizer.setupOptimizer(optimizationEndConditions)

# ============================================================================
class UpdatingPlotter():
    def __init__(self, temperatureModel, plotData, optimizer):
        # data
        self.temperatureModel = temperatureModel
        self.temperatureGroundTruth = plotData.getTemperatureModel()
        self.initialConditions = plotData.getInitialConditions()
        self.dt, self.maxTime = self.temperatureGroundTruth.getDtMaxT()
        
        self.optimizer = optimizer
        
        # set up containers
        self.plots = []
        
        # Set up plotter
        self.app = QtGui.QApplication([])
        self.win = QtGui.QMainWindow()
        self.layout = pg.LayoutWidget()
        self.win.setCentralWidget(self.layout)
        self.win.resize(1000,600)
        self.win.setWindowTitle('Optimization for motor: ' + motorName + ' using model: ' + modelName)
        pg.setConfigOptions(antialias=True)
        
        self.button = QtGui.QPushButton()
        self.button.clicked.connect(self.startOptimizer)

        # Default Params
        self.defaultColor = (0, 140, 170)
        self.auxColor = (190, 75, 50)
        pg.setConfigOption('foreground', 'k')
        pg.setConfigOption('background', 'w')
        
        self.lastStepCount = 0
        self.started = False
        
    def plotInitial(self, seedParameters):   
        self.temperatureModel.setParameters(seedParameters)
        times, outputs = self.temperatureModel.getTemperaturePlot(self.initialConditions, self.dt, self.maxTime)
        times, groundOutputs = self.temperatureGroundTruth.getTemperaturePlot()    
          
        # Main Plot
        p1 = pg.PlotWidget(title="alpha model")
        p1.setLabel('bottom', "time" )
        p1.addLegend()
        self.fittedPlot = p1.plot(x=times, y=outputs, pen=self.defaultColor)
        p1.plot(x=times, y=groundOutputs, pen=self.auxColor, name="ground")
        p1.showGrid(x = True, y = True, alpha = 0.3) 

        p2 = pg.PlotWidget(title="Cost")
        p2.setLabel('bottom', "step" )
        self.costPlot = p2.plot(y=[0], pen=self.defaultColor)
        p2.showGrid(x = True, y = True, alpha = 0.3)                                       
                    
        # layout stuff
        self.layout.addWidget(p1)
        self.plots.append(p1)
        self.layout.addWidget(p2)
        self.plots.append(p2)
        
        self.layout.nextRow()
        self.layout.addWidget(self.button)
        
        self.win.show()
        
    def updatePlot(self, currentParameters, currentCost):
        temperatureModel.setParameters(currentParameters)
        times, outputs = self.temperatureModel.getTemperaturePlot(self.initialConditions, self.dt, self.maxTime)
        self.fittedPlot.setData(times, outputs)
        
        valueHistory, costHistory = optimizer.getFullHistory()
        self.costPlot.setData(y=costHistory)
        
    def startOptimizer(self):
        if not self.started:
            self.started = True
            self.button.setText("started")
            print("starting")
            self.start_time = time.time()
            
    def optimizerIsRunning(self):
        return self.started
    
    def endOptimizer(self):
        self.started = False
    
        
def update():
    global optimizer, plotter, updateLock
    if plotter.optimizerIsRunning():
        if updateLock:
            # updateLock = False
            optimizer.optimizeNStepsOrUntilEndCondition(plotEveryNSteps)
            currentParameters, currentCost = optimizer.getCurrentStateAndCost()
            plotter.updatePlot(currentParameters, currentCost)
            
            if optimizer.hasReachedEndCondition():
                print("Time elapsed: " + str(time.time() - plotter.start_time))

                parameterHistory, costHistory = optimizer.getFullHistory();
                bestCostIndex = np.argmin(costHistory)
                finalParameters = parameterHistory[bestCostIndex, :]
                print(finalParameters)
                
                plotter.endOptimizer()
                
            # updateLock = True


updateLock = True
plotData = dataset[0]
plotter = UpdatingPlotter(temperatureModel, plotData, optimizer)
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

def main():
    plotter.plotInitial(seedParameters)
    
    runOptimizer()
    # temperatureModel.setParameters(finalParameters)
    # times, outputs = temperatureModel.getTemperaturePlot(initialConditions, dt, maxTime)
    # times, groundOutputs = temperatureGroundTruth.getTemperaturePlot()
    # plot(times, groundOutputs, outputs)

def runOptimizer():    
    start_time = time.time()
    while (not optimizer.hasReachedEndCondition()):
        optimizer.step();
        if (optimizer.stepCount % optimizer.printEveryNSteps == 0):
            optimizer.printDebug()
        if ((optimizer.stepCount > plotter.lastStepCount) and (optimizer.stepCount % plotEveryNSteps == 0)):
            currentParameters, currentCost = optimizer.getCurrentStateAndCost()
            print(1)
            plotter.updatePlot(currentParameters, currentCost)
            
    print("Time elapsed: " + str(time.time() - start_time))

    parameterHistory, costHistory = optimizer.getFullHistory();
    bestCostIndex = np.argmin(costHistory)
    finalParameters = parameterHistory[bestCostIndex, :]
    print(finalParameters)
    return finalParameters


        
        
if __name__ == '__main__':
    import sys
    plotter.plotInitial(seedParameters)
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
    