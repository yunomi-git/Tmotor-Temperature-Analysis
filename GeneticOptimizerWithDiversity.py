# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 14:04:09 2021

@author: Evan Yu
"""

from GeneticOptimizer import GeneticAlgorithmOptimizer, SimpleGAOptimizer
import numpy as np
from scipy.special import softmax


class SimpleGAOptimizerWithDiversity(SimpleGAOptimizer):
    def __init__(self, initialPopulation, costEvaluator, GAParameters):
        super().__init__(initialPopulation, costEvaluator, GAParameters)
        



# @dataclass
# class GAParametersWithDiversity(SimpleGAParameters):
    
    