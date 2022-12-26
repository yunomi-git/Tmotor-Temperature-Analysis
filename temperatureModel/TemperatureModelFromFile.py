# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 15:04:25 2022

@author: eyu
"""

import numpy as np
import pandas as pd


class TempModelFromFile:
    def __init__(self, filepath):
        super().__init__()
        
        data = pd.read_csv(filepath)
        self.times = np.array(data['time'].values.tolist())
        self.temps = np.array(data['temperature'].values.tolist())
        
    def getTemperaturePlot(self):
       return (self.times, self.temps)
   
    def getDtMaxT(self):
        dt = self.times[1] - self.times[0]
        maxTime = self.times[-1]
        return (dt, maxTime)