from bapsflib import lapd #Import erik's codes
import numpy as np #Standard python package for mathy stuff (everything from creating arrays to fourier transforms)
import matplotlib.pyplot as plt #Python package for plotting stuff
from matplotlib.animation import FuncAnimation

#GLOBAL VARIABLES

startFrame = 0
duration = 200

#Set to wherever your data file is located, this is from my folder
#data_file = 'C:/Users/mzhan/Desktop/VS Python/bapsflibtest/data/run65_Bdot_p35x_blockinglimiters_0degreestilt_12kV_3rdplane.hdf5'

#Uses erik's code to open  hdf5 file in python
#hdf5_file = lapd.File(data_file)    

#hdf5s are structured like windows explorer, where you have a hierarchy of groups and subgroups (similar to folders in windows).
#groups can also contain datasets, which are files containing actual data
#You can try running the following code to read out a list of subgroups in hdf5_file:
#for i in hdf5_file:
#    print(i)

#reads in an array of numbers from the hdf5 (code written by erik).
#board,channel are the board and channel on the DAQ
#shot_data will be 1-D if you only request one shot, 2-D for multiple shots.
board = 2
channel = 7
#requested_shots = [1,2,3]

#shot = hdf5_file.read_data(board, channel, add_controls=[('6K Compumotor', 1)]) #loads shot(s) from hdf5 into python
#shot_data = shot['signal'] #This gets the actual data, and makes it into an array

#There are other keys coded into shot_data, such as shot_data['shotnum'], which have additional info,
#but I've never used them.

#dimensions for shot_data are [shots, samples]. samples = data samples taken by DAQ

#the DAQ records all data samples in volts (since it's a computer duh), and will always be between -2.5 and 2.5 V
#To convert data to physical units, you have to know the electronics used for that probe

#plt.plot(shot_data[1,:]) #plot the first shot in the array, just to show it works

#plt.title('You can set plot titles like this')
#plt.show()
##this cell plots the probe trajectory over the plane.

#V_emiss = hdf5_file.read_data(board,channel, add_controls=[('6K Compumotor', 1)])
#[6K Compumotor, (1,2,3,4)]
#stop = V_emiss.shape[0]-1
#plt.figure()
#'xyz' or 'signal'
#plt.plot(V_emiss['xyz'][:,0],V_emiss['xyz'][:,1],'o')
#Marks starting and stopping location
#plt.plot(V_emiss['xyz'][0,0],V_emiss['xyz'][0,1],'g^',V_emiss['xyz'][stop,0],V_emiss['xyz'][stop,1],'r^')

#plt.xlabel('x position (cm)')
#plt.ylabel('y poisiiton (cm)')
#plt.title('Probe movement (starting at green and ending at red)')
#plt.show()

#hdf5_file.overview.print()


avg = []
#'signal': [shot number, time]
def getFrame(i, shot_data): #generate the ith frame
    idx = 0
    data_plot = np.zeros((35,20))
    for y in range(17, -18, -1): #iterate thru y coords
        for x in range(1,21,1): #iterate thru x coords
            data_plot[y,x-1] = shot_data[idx,i] #Set data_plot[x,y] to appropriate value
            idx+=10 #Increment idx by 10
    return data_plot
    

def animFrame(i, shot_data):
    data_plot = getFrame(i, shot_data)
    plt.imshow(data_plot)
    plt.title('run65, 3rd Plane, Board ' + str(board) + ', Ch ' + str(channel)+ ', Frame = ' + str(i))
    plt.subplots_adjust(left=0, right =0.6)

def avgPlot():
    plt.figure()
    for i in range(startFrame, startFrame+duration, 1):
        animFrame(i)
    framesAxis = np.arange(startFrame, startFrame+duration, 1)
    plt.plot(framesAxis, avg)
    plt.ylabel("Average Digitizer Value")
    plt.xlabel("Frame")
    plt.xlim([6990, 7210])
    plt.ylim([-0.02, 0.005])
    plt.show()

fileName = '3rdPlane_Board' + str(board) + '_Ch' + str(channel)

def savePlot(shot_data):
    fig, ax = plt.subplots()
    plt.xlabel('x (cm)')
    plt.ylabel('y (cm)')
    plt.xlim([-.5,20.5])
    plt.ylim([0, 35])
    animFrame(startFrame, shot_data)
    plt.colorbar()
    animation = FuncAnimation(fig = fig, func = animFrame, frames = np.arange(startFrame, startFrame+duration, 1), fargs = (shot_data,), interval = 1000)
    animation.save('C:/Users/mzhan/Desktop/VS Python/bapsflibtest/figures/' + fileName + '/' + fileName + '_F' + str(startFrame) + '.gif', dpi = 150, fps = 300, writer = 'ffmpeg')

#Returns a set of all distinct coordinates at which the probe makes stops at, tol = # of decimal places for tolerance
def getCoords(pos_data, tol):
    tracker = set()
    pos_data = np.around(pos_data, decimals = tol)
    for i in range(0, len(pos_data[:,0]), 1):
        for j in range(0, len(pos_data[:,1]), 1):
            tracker.add((pos_data[i,0], pos_data[j,1]))
    return tracker

#Returns the number of shots per location as well as output of getCoords
def getShotsPerLocation(pos_data, tol):
    tracker = getCoords(pos_data,tol)
    return len(pos_data[:,0])/len(tracker), tracker

def reshapeData(shot_data):
    #First reshape such that we index by (y,x,shotNum)
    #Then transpose such that it becomes (x,y,shotNum)
    return np.transpose(np.reshape(shot_data, (35,20,10,-1)), (1,0,2,3))

#Returns index given x,y values
def coordsToIndex(x, y, width):
#width is width in x direction
    return y*width+x

#Returns x,y coordinates given index
def indexToCoords(i, width):
    return i%width, int(i/width)

#shot = hdf5_file.read_data(board,channel, add_controls=[('6K Compumotor', 3)])
#[6K Compumotor, (1,2,3,4)]