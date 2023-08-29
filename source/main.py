from bapsflib import lapd
import numpy as np
import cupy as cp
from cupyx.scipy import signal as csig
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PolyCollection
import FFT as fft
import utils as bap
import plotter as plotter
import pandas as pd
import sys
import file

plt.style.use('ggplot')

def main():
    ########################
    #   GLOBAL VARIABLES   #
    ########################
    
    totalShots = 3360
    shotsPerPos = 10
    clockRate = 1e8
    
    pos_tol = 1
    startFrame = 5000
    duration = 250
    
    board = 2
    channel = 2
    #Folder Directory for Data    
    file_path1 = 'C:/Users/mzhan/Documents/GitHub/HDF5-LAPD-Processor/data/run65_Bdot_p35x_blockinglimiters_0degreestilt_12kV_3rdplane.hdf5'
    
    ############################
    #   IMPORT/LOAD THE DATA   #
    ############################
    
    file1 = file.file(file_path1, 0, board, channel)
    file1.readFile()
    file1.setYSize(35)
    file1.setXSize(20)
    file1.setTol(pos_tol)
    file1.getCoords()
    print(f'minX: {file1.minX}, maxX: {file1.maxX}, minY: {file1.minY}, maxY: {file1.maxY}')
    
    
    #plotter1 = plotter.plotter(file1, "tester")
    #plotter1.savePlot(startFrame, duration, "test")
    

if __name__ == "__main__":
    main()