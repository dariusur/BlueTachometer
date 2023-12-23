# BlueTachometer
BlueTachometer is a wireless hall sensor based tachometer that transmits measured RPM (revolutions per minute) via Bluetooth to PC. A Python script called "DataVisualizer" is used to plot incoming data from the tachometer (Fig. 1). After the measurement session is complete, the collected data can be saved in .csv format.

<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/screenshots/Fidget_spinner.png">
</div>
<div align="center">
  <i>Fig. 1. DataVisualizer Python script showing RPM measurement of a fidget spinner.</i>
</div>

## Installation
1. Assemble the circuit.
2. Download and extract the repository ZIP file.
3. Program the microcontroller using Microchip Studio.
4. Configure HC-05 Bluetooth module: Slave mode, 9600 baud rate (default settings).
5. Create a Python virtual environment that satisfies the requirements found in **DataVisualizer/requirements.txt**.
6. Attach a magnet to a rotating object to be measured.
7. Power up the tachometer.
8. Switch on Bluetooth on your PC and pair it with HC-05.
9. Run the DataVisualizer Python script.
10. Measure RPM.

## Hardware
1. ATtiny13 microcontroller.
2. HC-05 Bluetooth module (https://components101.com/wireless/hc-05-bluetooth-module).
3. A1120LUA-T Hall sensor.
4. 2 X Ceramic capacitor 100 nF.
5. 2 X Resistor 1 k.
6. Resistor 2 k.
7. Resistor 10 k.
8. NdFeB magnet Ø10x0.6mm N35 (not shown in schematic).

<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/schematics/BlueTachometer_schematic.png">
</div>
<div align="center">
  <i>Fig. 2. BlueTachometer schematic.</i>
</div>

## Implementation details
BlueTachometer uses a hall sensor to detect presence of a magnetic field. A magnet with its south pole facing the hall sensor is mounted on the rotating object that is to be measured. A south pole of sufficient strength turns the output on. Removal of the magnetic field turns the output off. Hall sensor output gives a digital signal and is open-drain. Upon activation it pulls the line LOW (active LOW signal). An external pullup resistor is used to pull the line HIGH when the hall sensor is deactivated. The measurement of the signal is performed by the MCU which executes the program shown in Fig. 3. To get a better visual understanding, Fig. 4 shows how the MCU measures the signal step by step. Essentially, the MCU measures the period of the signal. This is done by using a timer to increment a counter register. When the timer is stopped the MCU sends the counter value via UART to the Bluetooth module. The data is then transmitted to PC. Knowing the CPU clock frequency, the counter value can be converted to time (signal period) by calculating the CPU clock period and multiplying it by the counter value $T_{signal} = f_{cpu} * counter$. The signal frequency can be calculated by taking the inverse of the signal period $f_{signal} = T_{period}$. Finally, RPM can be obtained by multiplying the signal frequency by 60. All of this can be expressed in a simple formula $RPM = {f_{cpu} \over counter} * 60$. This is the equation that is used in the DataVisualizer script.

<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/flowchart/ATtiny_flowchart.png">
</div>
<div align="center">
  <i>Fig. 3. MCU program flowchart.</i>
</div>
<br></br>
<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/screenshots/signal_example.png">
</div>
<div align="center">
  <i>Fig. 4. Measurement algorithm shown on Hall sensor Vout signal captured with an oscilloscope.</i>
</div>

### DataVisualizer
DataVisualizer script uses 4 libraries: pyserial for communication with HC-05, matplotlib, numpy, pandas. 

## Specifications
* RPM measurement range: 0.017 to 9000000 RPM.

|Resolution|RPM|
|---|---|
|<5|18972|
|<1|8486|
|<0.5|6000|
|<0.1|2683|

* Data rate = 125 samples per second (5000 bits/s)

Resolution here means the minimal step by which RPM value can change. Meaning that when you are measuring, let's say, 18900 RPM, then the nearby RPM values that can be detected are either 18905 or 18895. The device cannot measure any values inbetween, say, 18902, or 18896. This is due to resolution limit which is set by the frequency of CPU clock (1.2 MHz). One important thing to mention here, is that the resolution depends on the RPM values that are being measured. The resolution is large at low RPM values and small at large RPM values. This characteristic is illustrated in Fig. 5. The graph shows that there are two limits, one is the 32 bit timer limit, which represents the greatest possible RPM value that can be stored within 32 bits. This limit could only be reached if MCU would perform the measurement on every clock cycle. However, instructions take time to execute, and in worst case scenario it takes 4 clock cycles to perform the measurement. This brings us to the other, measurement algorithm limit, which represents the greatest RPM value that the MCU can actually measure. Even though it is possible to measure up to 9000000 RPM, the resolution is so bad that the error is in the order of 100000s of RPM.

<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/graphs/resolution_graph.png">
</div>
<div align="center">
  <i>Fig. 5. Resolution graph, where timer count</i>
</div>

## Issues and notes for further development
* Currently there is a reliability issue, because there is no mechanism to track and prevent data loss during transmission. In addition there is no checking which byte of the four byte data packet is being read. When the first byte is being read, it is only assumed that it is the first byte. This leads to incorrect calculation of RPM. It seems like this issue can be avoided if the script is first started and only then the measurement is performed. The only time when this issue was observed is when the script is started during measurement.
* Measures only every other signal period. This issue comes from the fact that Attiny13 has only one timer and it is used for both the measurement and UART communication. If there were at least two timers, then one timer could be dedicated solely for measurement, and instead of stopping, it could simply be reset and continue to measure during communication.
* Data rate is slow. The communication speed could be improved if a greater baud rate was used. Also, pyserial read() function takes quite a significant time to execute (15-32 ms).
