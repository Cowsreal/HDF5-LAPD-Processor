from bapsflib import lapd
import sys
from file import file
from plotter import plotter

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
    channel = 1
    #Folder Directory for Data    
    file_path1 = 'C:/Users/mzhan/Documents/GitHub/HDF5-LAPD-Processor/data/run28_iisat_p31_blockinglimiters_12kV.hdf5'
    
    ############################
    #   IMPORT/LOAD THE DATA   #
    ############################
    
    file1 = file(file_path1, 0, board, channel)
    file1.readFile()
    file1.printOverview()
    #file1.setTol(pos_tol)
    #print("hi")
    #file1.getCoords()
    #print(f'minX: {file1.minX}, maxX: {file1.maxX}, minY: {file1.minY}, maxY: {file1.maxY}')

    #plotter1 = plotter(file1, "tester")
    #plotter1.savePlot(startFrame, duration, "test")


if __name__ == "__main__":
    main()