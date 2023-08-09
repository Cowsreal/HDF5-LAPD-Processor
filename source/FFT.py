
from bapsflib import lapd #Import erik's codes
import numpy as np #Standard python package for mathy stuff (everything from creating arrays to fourier transforms)
import matplotlib.pyplot as plt #Python package for plotting stuff
from matplotlib.animation import FuncAnimation
import utils as bap


#Generate FFT for a certain pixel at (x,y), shot_data must be post ['signal']
def getDigitizerData(shot_data, x, y, startFrame, duration, shotNum):
    data = []
    tempData = bap.reshapeData(shot_data)
    for i in range(startFrame, startFrame+duration+1, 1):
        data.append(tempData[x, y, shotNum, i])
    return data

#Generates FFT from digitizer data
def getFFT(data):
    return np.fft.fft(data)


