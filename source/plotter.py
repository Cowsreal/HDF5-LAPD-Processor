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
        
    def savePlot(self, startFrame, duration, name):
        """Generates a .gif of data animation

        Args:
            board (int): Board number
            channel (int): Channel number
            shot_data (array): 'signal' column of DF
            startFrame (int): starting frame
            duration (int): total number of frames requested
        """
        fig = plt.figure()
        plt.xlabel('x (cm)')
        plt.ylabel('y (cm)')
        self.animFrame(startFrame)
        plt.colorbar()
        animation = FuncAnimation(fig = fig, func = self.animFrame, frames = np.arange(startFrame, startFrame+duration, 1), interval = 1000)
        directory = f"C:/Users/mzhan/Documents/GitHub/HDF5-LAPD-Processor/figures/{self.figDir}/"
        filename = f"{name}_F{startFrame}.gif"
        Path(directory).mkdir(parents=True, exist_ok=True)
        animation.save(directory + filename, dpi = 150, fps = 300, writer = 'Pillow')
        
    def animFrame(self, i):
        """Helper function to generate the ith frame for savePlot(shot_data, startFrame, duration):

        Args:
            board (int): Board number
            channel (int): Channel number
            i (int): ith frame requested
            shot_data (array): 'signal' column of DF
            shotNum (int): shot number
        """
        data_plot = self.getFrameArr(i)
        plt.imshow(cp.transpose(data_plot, (1, 0)).get())
        plt.title(f'run65, 3rd Plane, Board {self.file.getBoard()}, Ch {self.file.getChannel()}, Frame = {i}')
        #Uncomment if needed:
        #plt.subplots_adjust(left = 1, right = 0.2)        
    
    def getFrameArr(self, i):
        """Helper function to generate values for the ith frame for animFrame(i, shot_data):

        Args:
            i (int): ith frame requested
            shot_data (array): 'signal' column of DF

        Returns:
            (2,2) array: digitizer values for each coordinate
        """
        shot_data = self.file.reshapeData()
        return shot_data[:, :, self.file.getShotNum(), i] 