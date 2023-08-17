from bapsflib import lapd
import numpy as np
import cupy as cp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PolyCollection
import FFT as fft
import utils as bap
import pandas as pd
import sys

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
    duration = 500
    
    
    ############################
    #   IMPORT/LOAD THE DATA   #
    ############################

    #Folder Directory
    file_path = 'C:/Users/mzhan/Documents/GitHub/HDF5-LAPD-Processor/data/run28_iisat_p31_blockinglimiters_12kV.hdf5'

    #bapsflib to read file
    hdf5_file = lapd.File(file_path)   

    #hdf5_file.overview.print()
    
    intfer_data = hdf5_file.read_msi('Interferometer array')
    
    print(intfer_data.dtype)
    #print(intfer_data['shotnum'])
    #print(intfer_data[])
    
    
    board = 1
    channel = 1

    data = hdf5_file.read_data(board, channel, add_controls=[('6K Compumotor', 1)])
    
    print(data.dtype)
    shot_data = cp.asarray(data['signal'])
    pos_data = data['xyz']
    
    shotsPerPos, shotsSet = bap.getShotsPerLocation(pos_data, pos_tol)

    #print(f"Shots per position: {shotsPerPos}, Number of positions: {len(shotsSet)} \n")
    print(shotsSet) #(-20, 15) -> (-6,-15)
    bap.savePlot(shot_data, startFrame, duration, 0)

    #Converts ['signal'] to [x,y,shotNum,frame(time)]
    #data = bap.reshapeData(shot_data)


    '''
    #Generates animation of XY shot data
    for i in range(0,16):
        bap.savePlot(shot_data)
        startFrame+=1000
    '''
    
    ################################
    #   POSITIONAL DATA ANALYSIS   #
    ################################

    #V_emiss = hdf5_file.read_data(board,channel, add_controls=[('6K Compumotor', 1)])
    #[6K Compumotor, (1,2,3,4)]
    #stop = V_emiss.shape[0]-1
    #plt.figure()
    #'xyz' or 'signal'
    #plt.plot(V_emiss['xyz'][:,0],V_emiss['xyz'][:,1],'o')
    #Marks starting and stopping location
    #plt.plot(V_emiss['xyz'][0,0],V_emiss['xyz'][0,1],'g^',V_emiss['xyz'][stop,0],V_emiss['xyz'][stop,1],'r^')
    #plt.show()
    
    #print("Calling getCoords!")
    #bap.getCoords(pos_data, pos_tol)
    #tracker = bap.getShotsPerLocation(pos_data, pos_tol)[1]
    #for i in tracker:
    #    print(i)

    ################
    #   FIND FFT   #
    ################
    
    
    '''         #3d plot
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    y = fft.getDigitizerData(shot_data, 0, 0, startFrame, duration, 0)
    y = fft.getFFT(y)
    n = len(y)
    x = np.fft.fftfreq(n, d = 1/clockRate)
    
    for i in range(700):
        xind = bap.indexToCoords(i, 20)[0]
        yind = bap.indexToCoords(i, 20)[1]
        y = fft.getDigitizerData(shot_data, xind, yind, startFrame, duration, 0)
        y = abs(fft.getFFT(y).get())
        ax.plot(x, y, i)
    ax.set_xlabel('Frequency')
    ax.set_ylabel('FFT Intensity')
    ax.set_zlabel('ith coordinate')
    plt.show()
    plt.plot(x, y)
    plt.show()
    '''
    
    
    
    
    '''
    dataGPU = cp.zeros((20,35))
    for i in range(700):
        xind = bap.indexToCoords(i, 20)[0]
        yind = bap.indexToCoords(i, 20)[1]
        val = fft.sumFFTPeak(shot_data, xind, yind, startFrame, duration, shotsPerPos)
        dataGPU[xind, yind] = val
    
    dataCPU = np.transpose(dataGPU.get(),(1,0))
    
    fig, ax = plt.subplots()
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.xlim([-.5,20.5])
    plt.ylim([0, 35])
    plt.imshow(dataCPU)
    plt.show()
    '''
    
    #signal package, band pass filter around rf frequency, use the butterworth filter
    #Langmuir Sweep, run16_sweeps_p31, how we get temperature profile
    
    #Look at run28_isat_p31_blocklimiters_12kV
    
if __name__ == "__main__":
    main()