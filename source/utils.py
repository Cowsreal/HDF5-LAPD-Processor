from bapsflib import lapd #Import erik's codes
import numpy as np #Standard python package for mathy stuff (everything from creating arrays to fourier transforms)
import matplotlib.pyplot as plt #Python package for plotting stuff
from matplotlib.animation import FuncAnimation
import cupy as cp
from sortedcollections import OrderedSet
from pathlib import Path


#GLOBAL VARIABLES

board = 1

channel = 1

#'signal': [shot number, time]
def getFrame(i, shot_data, shotNum):
    """Helper function to generate values for the ith frame for animFrame(i, shot_data):

    Args:
        i (int): ith frame requested
        shot_data (array): 'signal' column of DF

    Returns:
        (2,2) array: digitizer values for each coordinate
    """
    idx = shotNum
    data_plot = np.zeros((16,14))
    for y in range(0, 14, 1): #iterate thru y coords
        for x in range(0,16,1): #iterate thru x coords
            data_plot[x,y] = shot_data[idx,i] #Set data_plot[x,y] to appropriate value
            idx+=10 #Increment idx by 10
    return data_plot

def animFrame(i, shot_data, shotNum):
    """Helper function to generate the ith frame for savePlot(shot_data, startFrame, duration):

    Args:
        i (int): ith frame requested
        shot_data (array): 'signal' column of DF
        shotNum (int): shot number
    """
    data_plot = getFrame(i, shot_data, shotNum)
    plt.imshow(cp.transpose(data_plot, (1, 0)))
    plt.title('run28, isat, Board ' + str(board) + ', Ch ' + str(channel)+ ', Frame = ' + str(i))
    #Uncomment if needed:
    #plt.subplots_adjust(left = 1, right = 0.2)                     

fileName = f"isat_Board{board}_Ch{channel}"

def savePlot(shot_data, startFrame, duration, shotNum):
    """Generates a .gif of data animation

    Args:
        shot_data (array): 'signal' column of DF
        startFrame (int): starting frame
        duration (int): total number of frames requested
    """
    fig = plt.figure()
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    animFrame(startFrame, shot_data, shotNum)
    plt.colorbar()
    animation = FuncAnimation(fig = fig, func = animFrame, frames = np.arange(startFrame, startFrame+duration, 1), fargs = (shot_data, shotNum,), interval = 1000)
    directory = f"C:/Users/mzhan/Documents/GitHub/HDF5-LAPD-Processor/figures/{fileName}"
    filename = f"{fileName}_F{startFrame}.gif"
    Path(directory).mkdir(parents=True, exist_ok=True)
    animation.save(directory + filename, dpi = 150, fps = 300, writer = 'ffmpeg')

def getCoords(pos_data, tol):
    """
    Args:
        pos_data (array): 'xyz' column of DF
        tol (int): # of decimal places for same location tolerance

    Returns:
        tracker: set of all distinct coordinates at which the probe makes stops at
    """
    tracker = OrderedSet(set())
    pos_data = np.around(pos_data, decimals = tol)
    for i in range(0, len(pos_data[:,0]), 1):
        for j in range(0, len(pos_data[:,1]), 1):
            tracker.add((pos_data[i,0], pos_data[j,1]))
    return tracker

def getShotsPerLocation(pos_data, tol):
    """Returns the number of shots per location as well as output of getCoords

    Args:
        pos_data (array): 'xyz' column of DF
        tol (int): # of decimal places for same location tolerance

    Returns:
        getShotsPerLocation(pos_data, tol)[0] (int) : number of shots taken per location
        getShotsPerLocation(pos_data, tol)[1] (set) : output of getCoords(pos_data, tol):
    """
    tracker = getCoords(pos_data,tol)
    return len(pos_data[:,0])/len(tracker), tracker

def reshapeData(shot_data):
    """Transforms queue based 'signal' data in order to index with (x, y, shotNum, frame)

    Args:
        shot_data (array): 'signal' column of DF

    Returns:
        array : reshaped data
    """
    #First reshape such that we index by (y,x,shotNum,time)
    #Then transpose such that it becomes (x,y,shotNum,time)
    return cp.transpose(cp.reshape(shot_data, (16,14,10,-1)), (1,0,2,3))

def coordsToIndex(x, y, width):
    """Converts x, y coordinates to indexed (Increasing in left->right, down->up) coordinates 

    Args:
        x (int): x coordinate
        y (int): y coordinate
        width (int): Maximum x coordinate (1 based)

    Returns:
        int : Index
    """
    return y*width+x

def indexToCoords(i, width):
    """Converts index (Increasing in left->right, down->up) coordinates to x, y coordinates

    Args:
        i (int): index
        width (int): Maximum x coordinate (1 based)

    Returns:
        indexToCoords(i, width)[0] (int) : x coordinate
        indexToCoords(i, width)[1] (int) : y coordinate
    """
    return i%width, int(i/width)

#shot = hdf5_file.read_data(board,channel, add_controls=[('6K Compumotor', 3)])
#[6K Compumotor, (1,2,3,4)]