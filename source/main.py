from bapsflib import lapd
import sys
from file import File
from plotter import Plotter
import matplotlib.pyplot as plt
import numpy as np
import cupy as cp
import random

def main():
    ########################
    #   GLOBAL VARIABLES   #
    ########################
    
    totalShots = 6720
    shotsPerPos = 20
    clockRate = 1e8
    
    pos_tol = 2
    startFrame = 5000
    duration = 250
    
    board = 1
    channel = 1
    #Folder Directory for Data
    baseDir = 'C:/Users/mzhan/Documents/GitHub/HDF5-LAPD-Processor/data/'
    #run27_path = baseDir + 'run27_bdot_p27_blockinglimiters_12kV 2016-05-05 09.15.02.hdf5'
    run16_path = baseDir + 'run16_sweeps_p31.hdf5'
    #run28_path = baseDir + 'run28_iisat_p31_blockinglimiters_12kV.hdf5'
    #run65_3_path = baseDir + 'run65_Bdot_p35x_blockinglimiters_0degreestilt_12kV_3rdplane.hdf5'
    ############################
    #   IMPORT/LOAD THE DATA   #
    ############################
    
    run16 = File(run16_path, 0, board, channel)
    run16.setShotsPerPos(shotsPerPos)
    run16.readFile()
    run16.printOverview()
    run16.setXSize(21)
    run16.setYSize(16)
    run16.setDx(2)
    run16.setDy(2)
    run16.setTol(pos_tol)
    plt.figure()
    for i in range (0, 20):
        x = random.randint(0, 1000)
        slice = run16.reshapeData()[:, 8, 0, 12000 + x].get()
        xvals = np.linspace(0, 21, 21)
        plt.plot(xvals, slice)
    plt.xlabel("x (array indices)")
    plt.ylabel("Voltage (V)")
    plt.show()


    '''
    plt.figure()
    for i in range(0, 10):
        pixel = run16.reshapeData()[i, 8, 0, :].get()
        plt.plot(pixel, label = f'x = {i}, y = 8')
    
    plt.xlabel("Frame Number")
    plt.ylabel("Voltage (V)")
    plt.legend()
    plt.show()
    '''
    


    #run27.setShotsPerPos(shotsPerPos)
    #dat = run27.butter_bandpass(3.5e6, 6e6, clockRate, 5, 'bandpass')
    #dat = cp.asarray(dat) 
    

    #plotter27 = Plotter(run27, 'run27/run27_Board2_Ch1')
    #plotter27.addData(dat, 'Bandpass Filtered Data')
    #for i in range(startFrame, startFrame + 7000, 1000):
    #    plotter27.saveAnimPlot2D(i, duration, 'run27_Board2_Ch1', 1)
    
    #run28.setXSize(21)
    #run28.setYSize(16)
    #print(f'minX: {file1.minX}, maxX: {file1.maxX}, minY: {file1.minY}, maxY: {file1.maxY}')
    #run65_3 = file(run65_3_path, 0, 2, 1)
    #run65_3.readFile()
    



if __name__ == "__main__":
    main()