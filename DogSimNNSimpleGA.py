# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 17:43:38 2021

@author: Evan Yu
"""

import numpy as np;
from GeneticOptimizer import SimpleGAOptimizer, SimpleGAParameters
from Optimizer import OptimizationEndConditions
from FootModelNeuralNet import NNFootModelSimplest
from Simulation import BatchSimulation, Simulation, CostWeights, StochasticBatchSimulation
from DogUtil import DogModel, State, TaskMotion
# import matplotlib.pyplot as plt;
# import pyglet
# from pyglet.window import mouse
# from VisualizerSimulation import VisualizerSimulation
import pickle
import os
import time


subFolderName = "GA_NNSimpleModel_NewCostWeights"
prefix = "01-02-2022_10x10dataBatch"
suffix = "_01"
doRunOptimizer = True
# doRunOptimizer = False

startFromPreviousParameters = False
prevPrefix = "01-02-2022_10x10dataBatch"
prevSuffix = "_01"


simulationName = prefix + suffix
path = ".\\data\\" + subFolderName + "\\"
filename =  path + simulationName + '.pickle'

prevSimulationName = prevPrefix + prevSuffix
prevPath = ".\\data\\" + subFolderName + "\\"
prevFilename =  prevPath + prevSimulationName + '.pickle'
# -----------------------------------------------------------------------

def generateRandomInitialState():
    dogModel = DogModel()
    circleSample = np.random.rand(4,2)
    circleSample[:,0] = np.sqrt(circleSample[:,0] * DogModel.maximumFootDistanceFromIdeal)
    perturbations = np.zeros((4,2))
    perturbations[:,0] = circleSample[:,0] * np.cos(circleSample[:,1] * 2 * np.pi)
    perturbations[:,1] = circleSample[:,0] * np.sin(circleSample[:,1] * 2 * np.pi)
    perturbedFootState = dogModel.defaultFootState + perturbations
    
    state = State(perturbedFootState, 0.)
    return state
    
def generateInitialStatesList(numStates):
    dogModel = DogModel()
    initialCOM = np.array([-20.0, 0.01])
    initialFootState = dogModel.defaultFootState - initialCOM
    initialState = State(initialFootState, 0.)
    
    statesList = []
    statesList.append(initialState)
    for i in range(numStates-1):
        statesList.append(generateRandomInitialState())
    return statesList

def generateRandomTask(maxX, maxY, maxR):
    sample = np.random.rand(3)
    normedSample = sample / np.linalg.norm(sample)
    taskArray = np.array([maxX, maxY, maxR]) * normedSample
    return TaskMotion(taskArray[0], taskArray[1], taskArray[2])

def generateTaskMotionsList(numTasks, maxX, maxY, maxR):
    tasksList = []
    tasksList.append(TaskMotion(5., 0.1, 0.1))
    for i in range(numTasks-1):
        tasksList.append(generateRandomTask(maxX, maxY, maxR))
    return tasksList
    # return [TaskMotion(5., 0.1, 0.1)]
    # return [TaskMotion(5., 0.1, 0.1),
    #         TaskMotion(0.1, 4., 0.1),
    #         TaskMotion(-0.1, 0.1, 2.),
    #         TaskMotion(15., -0.1, -2.0),
    #         TaskMotion(-0.1, -10., 0.1),
    #         TaskMotion(0.1, -0.1, 10.)]

def generateInitialParametersAround(parametersCenter):
    initialParameters = np.random.rand(populationSize, numParameters) * scale - scale/2
    if parametersCenter is not None:
        initialParameters[0,numParameters] = np.zeros(numParameters)
        initialParameters += parametersCenter
    return initialParameters

def getPreviousParameters(filename):
    with open(filename, 'rb') as handle:
        simData = pickle.load(handle)
    parameterHistory = simData["parameterHistory"]
    costHistory = simData["costHistory"]    
        
    bestCostIndex = np.argmin(costHistory)
    finalParameters = parameterHistory[bestCostIndex, :]
    return finalParameters

# -----------------------------------------------------------------------

footModel = NNFootModelSimplest()
numParameters = footModel.getNumParameters()

numInitialStates = 10
numTasks = 10
maxTaskX = 20.
maxTaskY = 15.
maxTaskR = 10.

scale = 200.
populationSize = 50
prevParameters = None
if startFromPreviousParameters:
    prevParameters = getPreviousParameters(prevFilename)
    
initialParameters = generateInitialParametersAround(prevParameters)
initialStatesList = generateInitialStatesList(numInitialStates)
desiredMotionsList = generateTaskMotionsList(numTasks, maxTaskX, maxTaskY, maxTaskR)

batchStatesSize = 3
batchTasksSize = 3

costWeights = CostWeights(failureStepsAfterTermination=10000.,
                            failureSwingFootOutOfBounds=200.,
                            failureAnchoredFootOutOfBounds=200.,
                            failureComUnsupportedAtStart=200.,
                            failureComUnsupportedAtEnd=200.,
                            failureFootOutOfBoundsErrorFromIdeal=5.0,
                            failureComEndErrorFromCentroid=5.0,
                            
                            comNormTranslationErrorInitial = 2.,
                            comNormRotationErrorInitial = 2.,
                            comTranslationSmoothnessInitial= 0.1,
                            comRotationSmoothnessInitial = 0.1,
                            footNormErrorFromIdealInitial = 1.)

numSteps = 4

optimizationParameters = SimpleGAParameters(crossoverRatio=0.5, 
                                            mutationMagnitude=15.0,
                                            decreaseMutationMagnitudeEveryNSteps=50,
                                            mutationMagnitudeLearningRate=0.9,
                                            mutationChance=1.0,
                                            decreaseMutationChanceEveryNSteps=200,
                                            mutationChanceLearningRate=0.9,
                                            mutateWithNormalDistribution=False,
                                            mutationLargeCostScalingFactor=40.0,
                                            diversityChoiceRatio = 0.3,
                                            varianceMutationMaxMagnitude = 10.);  

optimizationEndConditions = OptimizationEndConditions(maxSteps=50000,
                                                      convergenceThreshold=0.0)

printEveryNSteps = 100

# ============================================================================


def main():
    print("Starting from old parameters: " + filename) 
    if os.path.exists(filename):
        overwrite = input("File path exists. Overwrite? <1> yes | <else> no: ")
        if (overwrite != '1'):
            print("Aborting")
            raise SystemExit
        else:
            print("Starting Simulation")
    if not os.path.isdir(path):
        os.mkdir(path)
        
    if doRunOptimizer:
        runOptimizer()

def runOptimizer():    
    # costEvaluator = BatchSimulation(initialStatesList = initialStatesList, 
    #                                 footModel = footModel, 
    #                                 desiredMotionsList = desiredMotionsList, 
    #                                 numSteps = numSteps, 
    #                                 costWeights = costWeights)
    costEvaluator = StochasticBatchSimulation(initialStatesList = initialStatesList, 
                                                footModel = footModel, 
                                                desiredMotionsList = desiredMotionsList, 
                                                numSteps = numSteps, 
                                                costWeights = costWeights,
                                                batchStatesSize = batchStatesSize, 
                                                batchTasksSize = batchTasksSize)
    optimizer = SimpleGAOptimizer(initialParameters, costEvaluator, optimizationParameters)
    optimizer.printEveryNSteps = printEveryNSteps
    optimizer.setOptimizationEndConditions(optimizationEndConditions)
    
    start_time = time.time()
    try:
        while (not optimizer.hasReachedEndCondition()):
            optimizer.step();
            if (optimizer.stepCount % optimizer.printEveryNSteps == 0):
                optimizer.printDebug()
    except KeyboardInterrupt:
        pass
    print("Time elapsed: " + str(time.time() - start_time))

    parameterHistory, costHistory = optimizer.getFullHistory();
    bestCostIndex = np.argmin(costHistory)
    finalParameters = parameterHistory[bestCostIndex, :]
    # finalParameters = parameterHistory[-1,:]
    
    print(finalParameters)
    
    simData = {}
    simData["parameterHistory"] = parameterHistory
    simData["costHistory"] = costHistory
    simData["optimizationParameters"] = optimizationParameters
    simData["optimizationPopulationSize"] = populationSize
    simData["optimizationEndConditions"] = optimizationEndConditions
    simData["simNumFootSteps"] = numSteps
    simData["simInitialStatesList"] = initialStatesList
    simData["simDesiredMotionsList"] = desiredMotionsList
    simData["finalParameters"] = finalParameters
    simData["footModel"] = footModel
    simData["simCostWeights"] = costWeights
    
    with open(filename, 'wb') as handle:
        pickle.dump(simData, handle)
    
    print("saved")
    
if __name__ == "__main__":
    main()
