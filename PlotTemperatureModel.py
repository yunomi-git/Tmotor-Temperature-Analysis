# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:13:06 2022

@author: eyu
"""

from HeatSource import HeatSource, HeatScript, ConductionHeatSource, RadiationSource, PowerSource
from HeatingItem import HeatingItem
from TemperatureModel import TemperatureModel
from CurrentScript import CurrentHeatingScript, CurrentTimeProfile
from TemperatureModelInstances import TempModelAlpha, TempModelOrig, TempModelBeta
import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
from TempModelPlotter import TempModelPlotter
from TemperatureModelFromFile import TempModelFromFile
import pyqtgraph as pg
from TimePlotCostEvaluator import TimePlotCostEvaluator
from TemperatureDataset import ak109Dataset
from MotorConstants import ak109MotorConstants
from FavoriteFittedParameters import AK109FittedParameters

runData = ak109Dataset[2]
initialConditions = runData.getInitialConditions()
motorConstants = ak109MotorConstants

temperatureGroundTruth = runData.getTemperatureModel()
dt, maxTime = temperatureGroundTruth.getDtMaxT()
times, outputsGround = temperatureGroundTruth.getTemperaturePlot()

parametersAlpha = AK109FittedParameters["alpha"].getVectorParameters()
temperatureModelAlpha = TempModelAlpha(motorConstants)
temperatureModelAlpha.setParameters(parametersAlpha)
timesAlpha, outputsAlpha = temperatureModelAlpha.getTemperaturePlot(initialConditions, dt, maxTime)

parametersOrig = AK109FittedParameters["orig"].getVectorParameters()
temperatureModelOrig = TempModelOrig(motorConstants)
temperatureModelOrig.setParameters(parametersOrig)
timesOrig, outputsOrig = temperatureModelOrig.getTemperaturePlot(initialConditions, dt, maxTime)

parametersBeta = AK109FittedParameters["beta"].getVectorParameters()
temperatureModelBeta = TempModelBeta(motorConstants)
temperatureModelBeta.setParameters(parametersBeta)
timesBeta, outputsBeta = temperatureModelBeta.getTemperaturePlot(initialConditions, dt, maxTime)

costEvaluator = TimePlotCostEvaluator(runData, temperatureModelAlpha)

print(costEvaluator.getCost(parametersAlpha))
print(costEvaluator.getCost(parametersAlpha))
            
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
pg.setConfigOption('foreground', 'k')
pg.setConfigOption('background', 'w')

defaultColor = (0, 140, 170)
auxColor = (190, 75, 50)
penWidth = 2
maxRowLength = 3        

    
rowIndex = 0
# layout.nextRow()

lines = []

layout.nextRow()
        
# Main Plot
p1 = pg.PlotWidget(title="alpha model")
p1.setBackground('w')
p1.setLabel('bottom', "time" , color=(0,0,0))
p1.setLabel('left', "temperature", units='C' )
p1.addLegend()
p1.plot(x=times, y=outputsGround, pen=pg.mkPen(auxColor, width=penWidth),  name="ground")
p1.plot(x=times, y=outputsAlpha, pen=pg.mkPen(defaultColor, width=penWidth), name="model")
p1.showGrid(x = True, y = True, alpha = 0.3)    

p2 = pg.PlotWidget(title="orig model")
p2.setBackground('w')
p2.setLabel('bottom', "time" )
p2.setLabel('left', "temperature", units='C' )
p2.addLegend()
p2.plot(x=times, y=outputsGround, pen=pg.mkPen(auxColor, width=penWidth), name="ground")
p2.plot(x=times, y=outputsOrig, pen=pg.mkPen(defaultColor, width=penWidth), name="model")
p2.showGrid(x = True, y = True, alpha = 0.3)   

p3 = pg.PlotWidget(title="beta model")
p3.setBackground('w')
p3.setLabel('bottom', "time" )
p3.setLabel('left', "temperature", units='C' )
p3.addLegend()
p3.plot(x=times, y=outputsGround, pen=pg.mkPen(auxColor, width=penWidth), name="ground")
p3.plot(x=times, y=outputsBeta, pen=pg.mkPen(defaultColor, width=penWidth), name="model")
p3.showGrid(x = True, y = True, alpha = 0.3)                                        
            
# layout stuff
layout.addWidget(p1)
layout.addWidget(p2)
layout.addWidget(p3)

win.show()
        
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()