# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 12:51:23 2021

@author: Evan Yu
"""
import numpy as np

def getRotationMatrix(angle):
    rad = np.radians(angle)
    c = np.cos(rad)
    s = np.sin(rad)
    rot = np.array([[c, -s],[s,c]])
    return rot

def getSignedVectorAngleFromRotation(v, rotation):
    rotationMat = getRotationMatrix(-rotation)
    v_rotated = rotationMat @ v
    angle = np.degrees(np.arctan2(v_rotated[1], v_rotated[0]))
    return angle

def getUnitVectorFromAngle(angle):
    rad = np.radians(angle)
    c = np.cos(rad)
    s = np.sin(rad)
    vector = np.array([c, s])
    return vector