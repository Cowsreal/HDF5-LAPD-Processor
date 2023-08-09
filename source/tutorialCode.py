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