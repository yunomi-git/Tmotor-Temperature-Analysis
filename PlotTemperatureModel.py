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
from TemperatureDataset import allDatasets
from MotorConstants import akMotorConstants
from FavoriteFittedParameters import allFittedMotorParameters
from pyqSlider import Slider

motorName = "AK606"
modelName = "alpha"
fitName = "fit2"

runData = allDatasets[motorName][1]
initialConditions = runData.getInitialConditions()
motorConstants = akMotorConstants

temperatureGroundTruth = runData.getTemperatureModel()
dt, maxTime = temperatureGroundTruth.getDtMaxT()
times, outputsGround = temperatureGroundTruth.getTemperaturePlot()

parametersAlpha = allFittedMotorParameters.getParametersForMotorModelFit(motorName, modelName, fitName)
temperatureModelAlpha = TempModelAlpha(motorConstants)
temperatureModelAlpha.setParameters(parametersAlpha)
timesAlpha, outputsAlpha = temperatureModelAlpha.getTemperaturePlot(initialConditions, dt, maxTime)

# parametersOrig = AK109FittedParameters["orig"].getVectorParametersForFit("fit4")
# temperatureModelOrig = TempModelOrig(motorConstants)
# temperatureModelOrig.setParameters(parametersOrig)
# timesOrig, outputsOrig = temperatureModelOrig.getTemperaturePlot(initialConditions, dt, maxTime)

# parametersBeta = AK109FittedParameters["beta"].getVectorParametersForFit("fit123")
# temperatureModelBeta = TempModelBeta(motorConstants)
# temperatureModelBeta.setParameters(parametersBeta)
# timesBeta, outputsBeta = temperatureModelBeta.getTemperaturePlot(initialConditions, dt, maxTime)

costEvaluator = TimePlotCostEvaluator(runData, temperatureModelAlpha)

print(costEvaluator.getCost(parametersAlpha))
print(costEvaluator.getCost(parametersAlpha))

class SliderOnPlotScale:
    def __init__(self, model, plotToTransform):
        self.slider1 = Slider(20, 1000)
        self.slider1.slider.setTickInterval(1)
        self.slider1.setLabelValue(50)
        self.slider1.slider.valueChanged.connect(self.sliderUpdate)
        
        self.slider2 = Slider(20, 4000)
        self.slider2.slider.setTickInterval(1)
        self.slider2.setLabelValue(49.5)
        self.slider2.slider.valueChanged.connect(self.sliderUpdate)
        
        self.slider3 = Slider(1, 1000)
        self.slider3.slider.setTickInterval(1)
        self.slider3.setLabelValue(49.5)
        self.slider3.slider.valueChanged.connect(self.sliderUpdate)
        
        self.slider4 = Slider(1, 1000)
        self.slider4.slider.setTickInterval(1)
        self.slider4.setLabelValue(49.5)
        self.slider4.slider.valueChanged.connect(self.sliderUpdate)
        
        self.plotToTransform = plotToTransform
        self.model = model
        
        
    def sliderUpdate(self):
        parameters = np.zeros(4)
        parameters[0] = self.slider1.x / 10
        parameters[1] = self.slider2.x / 10
        parameters[2] = self.slider3.x / 1000
        parameters[3] = self.slider4.x / 1000
        
        temperatureModelAlpha.setParameters(parameters)
        timesAlpha, outputsAlpha = temperatureModelAlpha.getTemperaturePlot(initialConditions, dt, maxTime)
        self.plotToTransform.setData(timesAlpha, outputsAlpha)
        
            
# set up containers
plots = []
layouts = []
sliders = []

# Set up plotter
app = QtGui.QApplication([])
win = QtGui.QMainWindow()
layout = pg.LayoutWidget()
win.setCentralWidget(layout)
win.resize(1000,600)
win.setWindowTitle('Plot for motor: ' + motorName + ' using model: ' + modelName)
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
p1 = pg.PlotWidget(title=modelName)
p1.setBackground('w')
p1.setLabel('bottom', "time" , color=(0,0,0))
p1.setLabel('left', "temperature", units='C' )
p1.addLegend()
p1.plot(x=times, y=outputsGround, pen=pg.mkPen(auxColor, width=penWidth),  name="ground")
modelPlot = p1.plot(x=times, y=outputsAlpha, pen=pg.mkPen(defaultColor, width=penWidth), name="model")
p1.showGrid(x = True, y = True, alpha = 0.3)    

sliders = SliderOnPlotScale(temperatureModelAlpha, modelPlot)

layout.nextRow()
layout.addWidget(sliders.slider1, colspan=1)
layout.addWidget(sliders.slider2, colspan=1)
layout.nextRow()
layout.addWidget(sliders.slider3, colspan=1)
layout.addWidget(sliders.slider4, colspan=1)

# p2 = pg.PlotWidget(title="orig model")
# p2.setBackground('w')
# p2.setLabel('bottom', "time" )
# p2.setLabel('left', "temperature", units='C' )
# p2.addLegend()
# p2.plot(x=times, y=outputsGround, pen=pg.mkPen(auxColor, width=penWidth), name="ground")
# p2.plot(x=times, y=outputsOrig, pen=pg.mkPen(defaultColor, width=penWidth), name="model")
# p2.showGrid(x = True, y = True, alpha = 0.3)   

# p3 = pg.PlotWidget(title="beta model")
# p3.setBackground('w')
# p3.setLabel('bottom', "time" )
# p3.setLabel('left', "temperature", units='C' )
# p3.addLegend()
# p3.plot(x=times, y=outputsGround, pen=pg.mkPen(auxColor, width=penWidth), name="ground")
# p3.plot(x=times, y=outputsBeta, pen=pg.mkPen(defaultColor, width=penWidth), name="model")
# p3.showGrid(x = True, y = True, alpha = 0.3)                                        
            
# layout stuff
layout.addWidget(p1)
# layout.addWidget(p2)
# layout.addWidget(p3)

win.show()
        
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()