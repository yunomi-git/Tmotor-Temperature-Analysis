# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 09:51:58 2022

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
from Optimizer import OptimizationEndConditions
import time
from TemperatureDataset import ak109Dataset
from MotorConstants import ak109MotorConstants


def generateInitialParametersAround(parametersCenter, scale):
    initialParameters = np.random.rand(populationSize, numParameters) * scale - scale/2
    if parametersCenter is not None:
        initialParameters[0,:] = np.zeros(numParameters)
        initialParameters += parametersCenter
    return initialParameters

def convertNamedParametersToParameters(namedParameters):
    return np.array([namedParameters["coilThermalMass"],
                     namedParameters["coilEnvConductivity"],
                     ])

# ============================================================================
# Model
dataset = [ak109Dataset[3]]
motorConstants = ak109MotorConstants

temperatureModel = TempModelOrig(motorConstants)
numParameters = temperatureModel.getNumParameters()

# Optimizer
costEvaluator = BatchTimePlotCostEvaluator(dataset, temperatureModel)

scale = 10.
populationSize = 10
namedParameters = {"coilThermalMass" : 85.,
                   "coilEnvConductivity" : 1.,
                   }

parameters = convertNamedParametersToParameters(namedParameters)
initialParameters = generateInitialParametersAround(parameters, scale)

optimizationParameters = SimpleGAParameters(crossoverRatio=0.5, 
                                            mutationMagnitude=10.,
                                            decreaseMutationMagnitudeEveryNSteps=50,
                                            mutationMagnitudeLearningRate=0.7,
                                            mutationChance=1.0,
                                            decreaseMutationChanceEveryNSteps=100,
                                            mutationChanceLearningRate=0.7,
                                            mutateWithNormalDistribution=False,
                                            mutationLargeCostScalingFactor=1.,
                                            diversityChoiceRatio = 0.3,
                                            varianceMutationMaxMagnitude = 1.,
                                            weightedMutationScaling = np.array([1., 0.1]));  

optimizationEndConditions = OptimizationEndConditions(maxSteps=500,
                                                      convergenceThreshold=0.0)

printEveryNSteps = 100

# ============================================================================
plotData = ak109Dataset[0]
temperatureGroundTruth = plotData.getTemperatureModel()
initialConditions = plotData.getInitialConditions()
dt, maxTime = temperatureGroundTruth.getDtMaxT()

def main():
    finalParameters = runOptimizer()
    temperatureModel.setParameters(finalParameters)
    times, outputs = temperatureModel.getTemperaturePlot(initialConditions, dt, maxTime)
    times, groundOutputs = temperatureGroundTruth.getTemperaturePlot()
    plot(times, groundOutputs, outputs)

def runOptimizer():    
    optimizer = SimpleGAOptimizer(initialParameters, costEvaluator, optimizationParameters)
    optimizer.printEveryNSteps = printEveryNSteps
    optimizer.setOptimizationEndConditions(optimizationEndConditions)
    
    start_time = time.time()
    while (not optimizer.hasReachedEndCondition()):
        optimizer.step();
        if (optimizer.stepCount % optimizer.printEveryNSteps == 0):
            optimizer.printDebug()

    print("Time elapsed: " + str(time.time() - start_time))

    parameterHistory, costHistory = optimizer.getFullHistory();
    bestCostIndex = np.argmin(costHistory)
    finalParameters = parameterHistory[bestCostIndex, :]
    print(finalParameters)
    return finalParameters

# set up containers
plots = []
layouts = []

# Set up plotter
app = QtGui.QApplication([])
win = QtGui.QMainWindow()
layout = pg.LayoutWidget()
win.setCentralWidget(layout)
win.resize(1000,600)
win.setWindowTitle('test')
pg.setConfigOptions(antialias=True)

# Default Params
defaultColor = (0, 255, 255)
auxColor = (255, 0, 255) 
def plot(times, groundOutputs, fittedOutputs):                 
    # Main Plot
    p1 = pg.PlotWidget(title="orig model")
    p1.setLabel('bottom', "time" )
    p1.addLegend()
    p1.plot(x=times, y=fittedOutputs, pen=defaultColor)
    p1.plot(x=times, y=groundOutputs, pen=auxColor, name="ground")
    p1.showGrid(x = True, y = True, alpha = 0.3)                                      
                
    # layout stuff
    layout.addWidget(p1)
    plots.append(p1)            
    
    win.show()
    
    return app, win, plots, layouts
        
if __name__ == '__main__':
    import sys
    main()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()