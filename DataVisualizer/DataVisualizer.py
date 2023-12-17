import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

COM_PORT = 'COM6'
BAUD_RATE = 9600
X_LIMIT = 200
Y_LIMIT = 100
SAVE_DIRECTORY = r"C:\Users\Darius\Desktop\\"

def on_close(event):
    plt.close('all')
    ser.close()

ser = serial.Serial(COM_PORT, BAUD_RATE)

x = np.linspace(0,0,0)
y = np.linspace(0,0,0)
fig, ax1 = plt.subplots()
ax2 = plt.twinx()
fig.canvas.mpl_connect('close_event', on_close)

line, = ax1.plot([], lw=1)
line.set_data(x, y)
text = fig.text(0.5,0.9, "0.000 Hz")

ax1.set_xlabel('Sample')
ax1.set_ylabel('Frequency, Hz')
ax1.set_xlim([0, X_LIMIT])
ax1.set_ylim([0, Y_LIMIT])
ax1.minorticks_on()
ax1.grid()
ax1.grid(which='minor', alpha=0.3)

ax2.set_ylim([0, Y_LIMIT])

fig.canvas.draw()   # note that the first draw comes before setting data 
plt.show(block=False)
fig.canvas.flush_events()

ser.flush()
while(True):
    if (ser.in_waiting > 0):
        ser_data = ser.read(4)
        break
        
    fig.canvas.draw()
    fig.canvas.flush_events()

sample_counter = 0

while (True):
    try:
        if (ser.in_waiting > 0):
            ser_data = ser.read(4)
            sample_counter = sample_counter + 1
            x = np.append(x, sample_counter)
            y = np.append(y, 1/((ser_data[0]|(ser_data[1]<<8)|(ser_data[2]<<16)|(ser_data[3]<<24)) * 8.33e-7))
            
            text.set_text('{:.3f} Hz'.format(y[sample_counter-1]))
            line.set_data(x, y)

            if (sample_counter > X_LIMIT):
                ax1.set_xlim([sample_counter-X_LIMIT+1, sample_counter])

            '''
            if (sample_counter > 100):
                line.set_data(x[(sample_counter-100):], y[(sample_counter-100):])
                ax1.set_xlim([sample_counter-99, sample_counter])
            else:
                line.set_data(x[:(sample_counter-1)], y[:(sample_counter-1)])
            # x = np.append(x, X_LIMIT+sample_counter)
            '''

        # redraw everything
        fig.canvas.draw()
        fig.canvas.flush_events()
    except:
        break


print("Number of samples: {}".format(y.size))
data_export = pd.DataFrame(data=y, index=x, columns=['f, Hz'])
print("----------------------------------")
print("Do you want to save data? (y/n)")
save = input()
while True:
    if save == 'y':
        print("Enter file name:")
        file_name = input()
        data_export.to_csv(SAVE_DIRECTORY + file_name + ".csv")
        break
    if save == 'n':
        break
print("Done!")