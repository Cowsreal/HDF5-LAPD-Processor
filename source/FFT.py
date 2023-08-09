
from bapsflib import lapd #Import erik's codes
import numpy as np #Standard python package for mathy stuff (everything from creating arrays to fourier transforms)
import matplotlib.pyplot as plt #Python package for plotting stuff
from matplotlib.animation import FuncAnimation
import utils as bap

def getDigitizerData(shot_data, x, y, startFrame, duration, shotNum):
    """Generate FFT for a certain pixel at (x,y), shot_data must be post ['signal']

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
    data = []
    tempData = bap.reshapeData(shot_data)
    for i in range(startFrame, startFrame+duration+1, 1):
        data.append(tempData[x, y, shotNum, i])
    return data

def getFFT(data):
    """Computes real valued FFT

    Args:
        data (array): one dimensional digitizer data

    Returns:
        array : real valued fft of input data
    """
    return np.fft.rfft(data)


