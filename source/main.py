from bapsflib import lapd #Import erik's codes
import numpy as np #Standard python package for mathy stuff (everything from creating arrays to fourier transforms)
import matplotlib.pyplot as plt #Python package for plotting stuff
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PolyCollection
import FFT as fft
import utils as bap

def main():
    #GLOBAL VARIABLES

    pos_tol = 2
    startFrame = 5000
    duration = 2000
    shotsPerPos = 10
    
    ############################
    #   IMPORT/LOAD THE DATA   #
    ############################

    #Folder Directory
    data_file = 'C:/Users/mzhan/Desktop/VS Python/bapsflibtest/data/run65_Bdot_p35x_blockinglimiters_0degreestilt_12kV_3rdplane.hdf5'

    #bapsflib to read file
    hdf5_file = lapd.File(data_file)   

    board = 2
    channel = 7

    shot = hdf5_file.read_data(board, channel, add_controls=[('6K Compumotor', 1)])
    shot_data = shot['signal']
    pos_data = shot['xyz']

    #shot_data[500,:]

    hdf5_file.overview.print()

    #Converts ['signal'] to [x,y,shotNum,frame(time)]
    data = bap.reshapeData(shot_data)


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
    '''
    plt.style.use('ggplot')
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x = np.arange(duration+1)  
    for i in range(700):
        xind = bap.indexToCoords(i, 20)[0]
        yind = bap.indexToCoords(i, 20)[1]
        y = fft.getDigitizerData(shot_data, xind, yind, startFrame, duration, 0)
        y = fft.getFFT(y)
        ax.plot(x, y, i)
    ax.set_xlabel('Frequency')
    ax.set_ylabel('FFT Intensity')
    ax.set_zlabel('ith coordinate')
    plt.show()
    plt.plot(x, y)
    plt.show()
    '''
    
if __name__ == "__main__":
    main()