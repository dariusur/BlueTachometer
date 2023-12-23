# BlueTachometer
BlueTachometer is a wireless hall sensor based tachometer that transmits measured RPM (revolutions per minute) via Bluetooth. A Python script called "DataVisualizer" is used to plot incoming data from the tachometer. After the measurement session is complete, the collected data can be saved in .csv format.

<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/screenshots/Fidget_spinner.png" width="400" height="400">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/graphs/PC_cooling_fan.png" width="400" height="400">
</div>
<div align="center">
  <i>Fig. 1. BlueTachometer schematic</i>
</div>

## Hardware
1. ATtiny13 microcontroller
2. HC-05 Bluetooth module (https://components101.com/wireless/hc-05-bluetooth-module)
3. A1120LUA-T Hall sensor
4. 2 X Ceramic capacitor 100 nF
5. 2 X Resistor 1 k
6. Resistor 2 k
7. Resistor 10 k
8. Magnet (not shown in schematic)

<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/schematics/BlueTachometer_schematic.png">
</div>
<div align="center">
  <i>Fig. 1. BlueTachometer schematic</i>
</div>


## Implementation details
BlueTachometer uses a hall sensor to detect presence of a magnetic field. A magnet attached to a rotating object triggers the hall sensor which outputs a digital signal. An external pullup resistor is used to pull the line high. Hall sensor output is open-drain so upon activation it pulls the line low (active low signal). The measurement of the signal is performed by the MCU which executes the following algorithm:

<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/flowchart/ATtiny_flowchart.png">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/screenshots/signal_example.png">
</div>
<div align="center">
  <i>Fig. 1. BlueTachometer schematic</i>
</div>

<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/screenshots/signal_example.png">
</div>
<div align="center">
  <i>Fig. 1. BlueTachometer schematic</i>
</div>

### Working principle

### Specs
* RPM measurement range: 0.017 to 9000000 RPM.

|Resolution|RPM|
|---|---|
|<5|18972|
|<1|8486|
|<0.5|6000|
|<0.1|2683|

In this range the tachometer can measure RPM with resolution of less than 5 RPM. Meaning that when you are measuring, let's say, 19000 RPM, then the nearby RPM values that can be detected are either 19005 or 18995. The device cannot measure any values inbetween, say, 19002, or 18996. This is due to resolution limit which is set by the frequency of CPU clock (1.2 MHz). One important thing to mention here, is that the resolution depends on the RPM values that are being measured. The resolution is large at low RPM values and small at large RPM values. This characteristic is illustrated in Fig. 1. The graph shows that there are two limits, one is the 32 bit timer limit, which represents the greatest possible RPM value that can be stored within 32 bits. This limit could only be reached if MCU would perform the measurement on every clock cycle. However, instructions take time to execute, and in worst case scenario it takes 4 clock cycles to perform the measurement. This brings us to the other, measurement algorithm limit, which represents the greatest RPM value that the MCU can actually measure. Even though I was able to reach this limit and measure 9000000 RPM by feeding the tachometer with a generated square wave, the resolution is so bad that the error is in the order of 100000s RPM.

<div align="center">
  <img src="https://github.com/dariusur/BlueTachometer/blob/main/misc/graphs/resolution_graph.png">
</div>
<div align="center">
  <i>Fig. 1. BlueTachometer schematic</i>
</div>

### ATtiny13


### HC-05

### Hall sensor
The tachometer uses a hall sensor to measure RPM. This means that a magnet with its south pole facing the hall sensor should be mounted on the rotating object that is to be measured. A south pole of sufficient strength turns the output on. Removal of the magnetic field turns the output off. The distributor did not specify the magnetic field strength of the magnet, but a quick search of similar magnets on the internet showed that similar N35 grade neodymium magnets have magnetic field strengths in the order of 100s or 1000s of gauss. This is enough to activate the hall sensor which at most requires 50 gauss.


## Issues
