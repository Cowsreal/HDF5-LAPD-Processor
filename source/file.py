from bapsflib import lapd
import numpy as np
import cupy as cp
from cupyx.scipy import signal as csig
from sortedcollections import OrderedSet
import scipy as sp

class file:
    def __init__(self, dir, shotNum = 0, board = 0, channel = 0):
        """Constructor for file class

        Args:
            shotNum (int): shotNum to be inspected
            dir (str): File path on disk
        """
        self.dir = dir
        self.shotNum = shotNum
        self.hdf5_file = lapd.File(dir)
        self.board = board
        self.channel = channel
        self.tol = 1
    
    ###########################
    #   GETTERS AND SETTERS   #
    ###########################
    
    def getBoard(self):
        """Returns current board value

        Returns:
            (int): Current board value
        """
        return self.board
    
    def setBoard(self, board):
        """Sets current board value

        Args:
            board (int): Board value to be set
        """
        self.board = board
        
    def getChannel(self):
        """Returns current channel value

        Returns:
            (int): Current channel value
        """
        return self.channel
    
    def setChannel(self, channel):
        """Sets current channel value

        Args:
            channel (int): Channel value to be set
        """
        self.channel = channel
    
    def getTol(self):
        """Returns the decimal tolerance for rounding off coordinate values

        Returns:
            (int): current tolerance
        """
        return self.tol
    
    def setTol(self, tol):
        """Sets the decimal tolerance for rounding off coordinate values

        Args:
            tol (int): Number of places after decimal to round
        """
        self.tol = tol

    def getShotNum(self):
        """Returns the shotNum

        Returns:
            (int): returns the currently set shotNum
        """
        return self.shotNum
    
    def setShotNum(self, shotNum):
        """Sets the shotNum

        Args:
            shotNum (int): New shotNum to be changed to
        """
        self.shotNum = shotNum

    def getXSize(self):
        """Gets the xSize of current data

        Returns:
            (int): The number of coordinates in position data in the x direction
        """
        return self.xSize

    def setXSize(self, xSize):
        """Sets the xSize of current data
        """
        self.xSize = xSize
    
    def getYSize(self):
        """Gets the ySize of current data

        Returns:
            (int): The number of coordinates in position data in the y direction
        """
        return self.ySize
    
    def setYSize(self, ySize):
        """Sets the ySize of current data
        """
        self.ySize = ySize
        
    def getDx(self):
        """Gets the dx, distance between each coordinate pass in the x direction
        """
        return self.dx
        
    def setDx(self, dx):
        """Sets the dx between each point scanned
        """
        self.dx = dx
        
    def getDy(self):
        """Gets the dy, distance between each coordinate pass in the y direction
        """
        return self.dy
        
    def setDy(self, dy):
        """Sets the dy between each point scanned
        """
        self.dy = dy

    #########################
    #   UTILITY FUNCTIONS   #
    #########################
        
    def printOverview(self):
        """Prints overview of current .hdf5 file
        """
        self.hdf5_file.overview.print()
    
    def readFile(self):
        """Creates and sets attributes data_main (requires board, channel), pos_data, and shot_data

        Args:
            board (int): Requested channel number
            channel (int): Requested channel number
        """
        self.data_main = self.hdf5_file.read_data(self.board, self.channel, add_controls=[('6K Compumotor', 1)])
        self.pos_data = cp.asarray(self.data_main['xyz'])
        self.shot_data = cp.asarray(self.data_main['signal'])
    
    def getCoords(self):
        """Sets attribute .coordsList to an ordered set of all coordinates the probe visits, also updates maxX, minX, maxY, minY
        Args:
            pos_data (array): 'xyz' column of DF
            tol (int): # of decimal places for same location tolerance

        Returns:
            coordsList: set of all distinct coordinates at which the probe makes stops at
        """
        temp = cp.copy(cp.around(self.pos_data, decimals = self.tol)).get()
        self.coordsList = OrderedSet(set())
        self.maxX = -99999
        self.minX = 99999
        self.maxY = -99999
        self.minY = 99999
        
        def minMaxUpdater(i, j):
            if temp[i,0] > self.maxX:
                self.maxX = temp[i,0]
            if temp[i,0] < self.minX:
                self.minX = temp[i,0]
            if temp[j,1] > self.maxY:
                self.maxY = temp[j,1]
            if temp[j,1] < self.minY:
                self.minY = temp[j,1]

        x = len(temp[:,0])
        y = len(temp[:,1])
        for i in range(0, x, 1):
            for j in range(0, y, 1):
                minMaxUpdater(i, j)
                self.coordsList.add((temp[i, 0], temp[j, 1]))
        return self.coordsList

    def getShotsPerLocation(self):
        """Returns the number of shots per location as well as output of getCoords

        Args:
            pos_data (array): 'xyz' column of DF
            tol (int): # of decimal places for same location tolerance

        Returns:
            (int) : number of shots taken per location
        """
        if not hasattr(self, 'coordsList'):
            self.getCoords()
        return len(self.pos_data)//len(self.coordsList)
        
    def coordsToIndex(self, x, y, width):
        """Converts x, y coordinates to indexed (Increasing in left->right, down->up) coordinates 

        Args:
            x (int): x coordinate
            y (int): y coordinate
            width (int): Maximum x coordinate (1 based)

        Returns:
            int : Index
        """
        return y*width*(1/self.dy)+x*(1/self.dx)
    
    def indexToCoords(self, i, width):
        """Converts index (Increasing in left->right, down->up) coordinates to x, y coordinates

        Args:
            i (int): index
            width (int): Maximum x coordinate (1 based)

        Returns:
            indexToCoords(i, width)[0] (int) : x coordinate
            indexToCoords(i, width)[1] (int) : y coordinate
        """
        return i%width*self.dx, (i//width)*self.dy
    
    def reshapeData(self, data):
        """Transforms queue based 'signal' data in order to index with (x, y, shotNum, frame)

        Args:
            shot_data (array): 'signal' column of DF

        Returns:
            array : reshaped data
        """
        #First reshape such that we index by (y,x,shotNum,time)
        #Then transpose such that it becomes (x,y,shotNum,time)
        if data is self.shot_data:
            return cp.transpose(cp.reshape(data, (self.getYSize(), self.getXSize(), self.getShotsPerLocation(), -1)), (1,0,2,3))
        else:
            return cp.transpose(cp.reshape(data, (self.getYSize(), self.getXSize(), -1)), (1,0,2))

    def getFrameArr(self, i):
        """Helper function to generate values for the ith frame for animFrame(i, shot_data):

        Args:
            i (int): ith frame requested
            shot_data (array): 'signal' column of DF

        Returns:
            (2,2) array: digitizer values for each coordinate
        """
        shot_data = self.reshapeData(self.shot_data)
        return shot_data[:, :, self.getShotNum(), i] 

    #####################
    #   FFT Functions   #
    #####################
    
    def getDigitizerData(self, x, y, startFrame, duration):
        """Generate array of digitizer data for a certain pixel at (x,y), shot_data must be 'signal' DF

        Args:
            shot_data (array): 'signal' column of DF
            x (int): x coordinate
            y (int): y coordinate
            startFrame (int): requested starting frame
            duration (int): duration of data in frames

        Returns:
            array : one dimensional digitizer data
        """
        
        data = cp.zeros(shape = (duration+1,))
        tempData = self.reshapeData(self.shot_data)
        for i in range(startFrame, startFrame+duration+1, 1):
            data[i-startFrame] = tempData[x, y, self.getShotNum(), i]
        return data
    
    def getFFT(self, data):
        """Computes the FFT of the data

        Args:
            data (cp.ndarray): Data to be FFT'd
            axis (int, optional): Axis along which to compute FFT. Defaults to 1.

        Returns:
            cp.ndarray : Real valued FFT of data
        """
        return cp.fft.rfftn(data)
    
    def sumFFTPeak(self, x, y, startFrame, duration):
        sumArr = cp.zeros(self.getShotsPerLocation())
        for i in range(0, self.getShotsPerLocation()):
            sumArr[i] = cp.max(cp.absolute(self.getDigitizerData(x, y, startFrame, duration, i)))
        sum =  cp.sum(sumArr)
        return sum

    def butter_bandpass(self, lowCut, highCut, fs, order, btype):
        """Computes butter band pass coefficients and applies them to file.shot_data and returns result

        Args:
            lowCut (_type_): _description_
            highCut (_type_): _description_
            fs (_type_): _description_
            order (_type_): _description_
            btype (_type_): _description_

        Returns:
            numpy.ndarray : Filtered Data
        """
        b, a = sp.signal.butter(N = order, Wn = (lowCut, highCut), btype = btype, fs = fs)
        shot_data = self.reshapeData(self.shot_data)
        shot_data = shot_data[:,:,self.getShotNum(),:]
        return sp.signal.filtfilt(b, a, shot_data.get(), axis = -1)