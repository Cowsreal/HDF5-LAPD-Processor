from bapsflib import lapd
import sys
from file import file
from plotter import plotter
import matplotlib.pyplot as plt
import numpy as np
import cupy as cp

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
    
    board = 1
    channel = 1
    #Folder Directory for Data    
    file_path1 = 'C:/Users/mzhan/Documents/GitHub/HDF5-LAPD-Processor/data/run28_iisat_p31_blockinglimiters_12kV.hdf5'
    
    ############################
    #   IMPORT/LOAD THE DATA   #
    ############################
    
    file1 = file(file_path1, 0, board, channel)
    file1.readFile()
    file1.setXSize(21)
    file1.setYSize(16)
    #print(f'minX: {file1.minX}, maxX: {file1.maxX}, minY: {file1.minY}, maxY: {file1.maxY}')
    temp = file1.reshapeData()
    arr = cp.zeros((temp.shape[0], temp.shape[3]))
    for i in range(10):
        arr += temp[:, 8, i, :]
    arr /= 10
    
    startFrame = 4792
    x = np.arange(200)
    fig, ax = plt.subplots(1)
    for i in range(10):
        temp = arr[i,startFrame:startFrame+200].get()
        ax.plot(x, temp)
        #ax[i//5, i % 5].set_title(f'x = {i}')
    for i in range(12):
        ax.axvline(5*i+i//3, color = 'k')
    for i in range(12):
        ax.axvline(63+5*i+i//3, color = 'k')
    for i in range(12):
        ax.axvline(126+5*i+i//3, color = 'k')
    plt.show()
    
    
    fig, ax = plt.subplots(2,5)
    x = np.arange(-20,22,2)
    for k in range(0, 10):
        for i in range(0, 6, 1):
            ax[k//5, k%5].plot(x, arr[:, startFrame + 5*k + k // 3 + i].get(), alpha = .16*i+.16, color = 'k')
            ax[k//5, k%5].set_title(f"Start Frame = {startFrame + 5 * k + k // 3}")
            ax[k//5, k%5].set_xlabel('x (cm)')
            ax[k//5, k%5].set_ylabel('Mean isat value')
    plt.show()
    
    #file1.setTol(pos_tol)
    #print("hi")
    #file1.getCoords()

    #plotter1 = plotter(file1, "tester")
    #plotter1.savePlot(startFrame, duration, "test")


if __name__ == "__main__":
    main()