import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# USER PARAMETERS
COM_PORT = 'COM6' # your COM port
X_LIMIT = 100 # graph width
Y_LIMIT = 5000 # graph height
SAVE_DIRECTORY = r"C:\Users\Darius\Desktop\\"

# CONSTANTS - DO NOT CHANGE!
BAUD_RATE = 9600
MCU_CLK_FREQUENCY = 1.2e6 # 833 ns

# Called when the graph is closed.
def on_close(event):
    plt.close('all') # close all figure windows
    ser.close() # close serial port

ser = serial.Serial(COM_PORT, BAUD_RATE) # begin serial communication 

### GRAPH CONFIGURATION START
x = np.linspace(0,0,0) # create an empty array
y = np.linspace(0,0,0) # create an empty array
fig, ax1 = plt.subplots()
ax2 = plt.twinx()
fig.canvas.mpl_connect('close_event', on_close)

line, = ax1.plot([], lw=1)
line.set_data(x, y)
#text = fig.text(0.5,0.9, "0.000 Hz")
text = fig.text(0.5,0.9, "0.000 RPM")

ax1.set_xlabel('Sample')
#ax1.set_ylabel('Frequency, Hz')
ax1.set_ylabel('RPM')
ax1.set_xlim([0, X_LIMIT])
ax1.set_ylim([0, Y_LIMIT])
ax1.minorticks_on()
ax1.grid()
ax1.grid(which='minor', alpha=0.3)

ax2.set_ylim([0, Y_LIMIT])

fig.canvas.draw()   # the first draw comes before setting data 
plt.show(block=False)
fig.canvas.flush_events()
### GRAPH CONFIGURATION END

# Discard the first measurement, because its always close to 0
while(True):
    try:
        if (ser.in_waiting > 0):
            ser_data = ser.read(4)
            break
        
        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        break

sample_counter = 0

### MAIN LOOP START
while (True):
    try:
        data_in = ser.in_waiting
        if ((data_in % 4 == 0) and (data_in != 0)):
            ser_data = ser.read(data_in)
            for i in range(0, int(data_in/4)):    
                sample_counter = sample_counter + 1
                x = np.append(x, sample_counter)
                #y = np.append(y, MCU_CLK_FREQUENCY / (ser_data[i*4]|(ser_data[i*4+1]<<8)|(ser_data[i*4+2]<<16)|(ser_data[i*4+3]<<24))) # convert time to frequency
                y = np.append(y, MCU_CLK_FREQUENCY / (ser_data[i*4]|(ser_data[i*4+1]<<8)|(ser_data[i*4+2]<<16)|(ser_data[i*4+3]<<24)) * 60) # convert time to RPM
            
            #text.set_text('{:.3f} Hz'.format(y[sample_counter-1])) # update text Hz
            text.set_text('{:.3f} RPM'.format(y[sample_counter-1])) # update text RPM
            line.set_data(x, y) # update data

            # when sample_counter exceeds X_LIMIT move the graph window right to show the most recent sample
            if (sample_counter > X_LIMIT):
                ax1.set_xlim([sample_counter-X_LIMIT+1, sample_counter])

        # redraw everything
        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        break

# Export collected data
print("Number of samples: {}".format(y.size))
#data_export = pd.DataFrame(data=y, index=x, columns=['f, Hz'])
data_export = pd.DataFrame(data=y, index=x, columns=['RPM'])
print("----------------------------------")
print("Do you want to save data? (y/n)")
save = input()
if save == 'y':
    print("Enter file name:")
    file_name = input()
    data_export.to_csv(SAVE_DIRECTORY + file_name + ".csv")

print("Done!")
### MAIN LOOP END