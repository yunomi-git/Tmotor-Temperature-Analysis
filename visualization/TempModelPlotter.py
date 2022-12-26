# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:28:21 2022

@author: eyu
"""

import pandas as pd
import statistics as stat
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.dockarea import *
from visualization.pyqSlider import Slider

class SliderWithLines:
    def __init__(self, lines, minVal, maxVal):
        self.slider = Slider(minVal, maxVal)
        self.slider.slider.valueChanged.connect(self.sliderUpdate)
        self.lines = lines
        
    def sliderUpdate(self):
        idx = self.slider.x
        for line in self.lines:
            line.setValue(idx)

class TempModelPlotter():
    def __init__(self, name, outputNames, times, outputs):
        self.name = name
        self.outputNames = outputNames
        self.times = times
        self.outputs = outputs
        self.numItemsToPlot = len(outputNames)
            
        # set up containers
        self.plots = []
        self.docks = []
        self.layouts = []
        self.sliders = []
        
        # Set up plotter
        self.app = QtGui.QApplication([])
        self.win = QtGui.QMainWindow()
        self.layout = pg.LayoutWidget()
        self.win.setCentralWidget(self.layout)
        self.win.resize(1000,600)
        self.win.setWindowTitle(self.name)
        pg.setConfigOptions(antialias=True)
        
        # Default Params
        self.defaultColor = (0, 255, 255)
        self.mirrorColor = (255, 0, 255)
        self.maxRowLength = 3        

    def plot(self):
        rowIndex = 0
        # layout.nextRow()
        
        lines = []
        slider = SliderWithLines(lines, 0, self.times[-1])
        
        self.layout.addWidget(slider.slider, colspan=2)
        self.layout.nextRow()
        
        for i in range(self.numItemsToPlot):
            # Main Plot
            p1 = pg.PlotWidget(title=self.outputNames[i])
            p1.setLabel('bottom', "time" )
            p1.addLegend()
            if (self.numItemsToPlot == 1):
                p1.plot(x=self.times, y=self.outputs, pen=self.defaultColor)
            else:
                p1.plot(x=self.times, y=self.outputs[i,:], pen=self.defaultColor)
            p1.showGrid(x = True, y = True, alpha = 0.3)                                        
            
            # Line on x
            line = pg.InfiniteLine(angle=90, movable=False, pos=0)
            p1.addItem(line)
            lines.append(line)
            
            # layout stuff
            self.layout.addWidget(p1)
            self.plots.append(p1)            
            
            rowIndex += 1
            if (rowIndex == 3):
                rowIndex = 0
                self.layout.nextRow()
                
        slider.lines = lines
            
        # Save everything
        self.sliders.append(slider)
                
        self.win.show()