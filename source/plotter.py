import numpy as np
import cupy as cp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PolyCollection
from pathlib import Path

plt.style.use('ggplot')

class plotter:
    def __init__(self, file, dir):
        self.file = file
        self.figDir = dir      #figDir is figure directory after .../figures/... 
        self.dataArr = []
        self.dataArr.append((self.file.reshapeData(self.file.shot_data), 'File Data'))

    def addData(self, data, desc = 'Undefined'):
        """Adds pair to self.dataArr where the first element is the data and the second element is the description

        Args:
            data (cupy.ndarray): Data to be added
            desc (str, optional): Description for added data. Defaults to 'Undefined'.
        """
        self.dataArr.append((self.file.reshapeData(data), desc))
        
    def printDataArr(self):
        for i, data in enumerate(self.dataArr):
            print(f'Index: {i}, Description: {data[1]} \n')

    def saveAnimPlot2D(self, startFrame, duration, name, dataArridx = 0):
        """Generates a .gif of data animation

        Args:
            startFrame (int): starting frame
            duration (int): total number of frames requested
            name (str): name of the gif and subfolder
            dataArridx (int): index of the self.dataArr to be plotted
        """
        fig = plt.figure()
        plt.xlabel('x (cm)')
        plt.ylabel('y (cm)')
        self.animFrame(startFrame, dataArridx)
        plt.colorbar()
        animation = FuncAnimation(fig = fig, func = self.animFrame, fargs = (dataArridx, ), frames = np.arange(startFrame, startFrame+duration, 1), interval = 1000)
        directory = f"C:/Users/mzhan/Documents/GitHub/HDF5-LAPD-Processor/figures/{self.figDir}/"
        filename = f"{name}_F{startFrame}.gif"
        Path(directory).mkdir(parents=True, exist_ok=True)
        animation.save(directory + filename, dpi = 150, fps = 300, writer = 'Pillow')
        
    def animFrame(self, i, idx):
        """Helper function to generate the ith frame for saveAnimPlot2D

        Args:
            board (int): Board number
            channel (int): Channel number
            i (int): ith frame requested
            shot_data (array): 'signal' column of DF
            shotNum (int): shot number
        """

        data_plot = self.getFrameArr(i, idx)
        plt.imshow(cp.transpose(data_plot, (1, 0)).get())
        plt.title(f'run65, 3rd Plane, Board {self.file.getBoard()}, Ch {self.file.getChannel()}, Frame = {i}')
        #Uncomment if needed:
        #plt.subplots_adjust(left = 1, right = 0.2)
    
    def getFrameArr(self, i, idx = 0):
        if not hasattr(self, 'temp'):
            self.temp1 = self.file.reshapeData(self.dataArr[idx][0])
        return self.temp1[:, :, i]