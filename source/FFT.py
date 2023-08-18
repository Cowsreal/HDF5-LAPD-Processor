
from bapsflib import lapd
import numpy as np
import cupy as cp
import cupyx as cpx
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import utils as bap

def getDigitizerData(shot_data, x, y, startFrame, duration, shotNum):
    """Generate digitizer data for a certain pixel at (x,y), shot_data must be post ['signal']

    Args:
        shot_data (array): 'signal' column of DF
        x (int): x coordinate
        y (int): y coordinate
        startFrame (int): requested starting frame
        duration (int): duration of data in frames
        shotNum (int): requested shot number

    Returns:
        array : one dimensional digitizer data
    """
    
    data = cp.zeros(shape = (duration+1,))
    tempData = bap.reshapeData(shot_data)
    for i in range(startFrame, startFrame+duration+1, 1):
        data[i-startFrame] = tempData[x, y, shotNum, i]
    return data

def getFFT(data):
    """Computes real valued FFT

    Args:
        data (array): one dimensional digitizer data

    Returns:
        array : real valued fft of input data
    """
    return cp.fft.rfft(data)

def sumFFTPeak(shot_data, x, y, startFrame, duration, totalShots):
    sumArr = cp.zeros(totalShots)
    for i in range(0, totalShots):
        sumArr[i] = cp.max(cp.absolute(getDigitizerData(shot_data, x, y, startFrame, duration, i)))
    sum =  cp.sum(sumArr)
    return sum

def butter_bandpass(shot_data, lowCut, highCut, fs, order):
    a, b = cpx.scipy.signal.butter(order, (lowCut, highCut), 'bandpass', fs)
    return cpx.scipy.signal.filtfilt(b, a, shot_data[:,:], axis=1)
    
    