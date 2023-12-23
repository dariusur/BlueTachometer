# BlueTachometer
BlueTachometer is a wireless hall sensor based tachometer that transmits measured RPM (revolutions per minute) via Bluetooth to PC. A Python script called "DataVisualizer" is used to plot incoming data from the tachometer (Fig. 1). After the measurement session is complete, the collected data can be saved in .csv format.

<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/screenshots/Fidget_spinner.png">
</div>
<div align="center">
  <i>Fig. 1. DataVisualizer Python script showing RPM measurement of a fidget spinner.</i>
</div>

## Installation
1. Assemble the circuit
2. Download repo
3. Program the microcontroller using microchip studio
4. Setup Hc-05 Bluetooth module
5. Create a virtual environment that satisfies the requirements found in ///'requirements.txt'.
6. Launch the script
7. Power up the tachometer
8. attach a magnet to a rotating object
9. Measure RPM!

## Hardware
1. ATtiny13 microcontroller
2. HC-05 Bluetooth module (https://components101.com/wireless/hc-05-bluetooth-module)
3. A1120LUA-T Hall sensor
4. 2 X Ceramic capacitor 100 nF
5. 2 X Resistor 1 k
6. Resistor 2 k
7. Resistor 10 k
8. NdFeB magnet Ø10x0.6mm N35 (not shown in schematic)

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

### Specifications
* RPM measurement range: 0.017 to 9000000 RPM.

|Resolution|RPM|
|---|---|
|<5|18972|
|<1|8486|
|<0.5|6000|
|<0.1|2683|

Resolution here means the minimal step by which RPM value can change. Meaning that when you are measuring, let's say, 18900 RPM, then the nearby RPM values that can be detected are either 18905 or 18895. The device cannot measure any values inbetween, say, 18902, or 18896. This is due to resolution limit which is set by the frequency of CPU clock (1.2 MHz). One important thing to mention here, is that the resolution depends on the RPM values that are being measured. The resolution is large at low RPM values and small at large RPM values. This characteristic is illustrated in Fig. 5. The graph shows that there are two limits, one is the 32 bit timer limit, which represents the greatest possible RPM value that can be stored within 32 bits. This limit could only be reached if MCU would perform the measurement on every clock cycle. However, instructions take time to execute, and in worst case scenario it takes 4 clock cycles to perform the measurement. This brings us to the other, measurement algorithm limit, which represents the greatest RPM value that the MCU can actually measure. Even though it is possible to measure up to 9000000 RPM, the resolution is so bad that the error is in the order of 100000s of RPM.

<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/graphs/resolution_graph.png">
</div>
<div align="center">
  <i>Fig. 5. Resolution graph, where timer count</i>
</div>

## Issues
Reliability issue, packet identification
Measures only every other period
slow com speed
