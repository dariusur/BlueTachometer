# BlueTachometer
BlueTachometer, as the name suggests, is a wireless tachometer that transmits measured RPM (revolutions per minute) via Bluetooth. A Python script called "DataVisualizer" is used to monitor incoming data from the tachometer. After the measurement session is complete, the collected data can be saved in .csv format.
## Hardware
1. ATtiny13 microcontroller
2. HC-05 Bluetooth module
3. A1120LUA-T Hall sensor
4. Magnet (not shown in schematic)
## Description
RPM measurement range: 0.000279 - 200 kHz?
Resolution: 32 bits

### ATtiny13


### HC-05

### Hall sensor
The tachometer uses a hall sensor to measure RPM. This means that a magnet with its south pole facing the hall sensor should be mounted on the rotating object that is to be measured. A south pole of sufficient strength turns the output on. Removal of the magnetic field turns the output off. The distributor did not specify the magnetic field strength of the magnet, but a quick search of similar magnets on the internet showed that similar N35 grade neodymium magnets have magnetic field strengths in the order of 100s or 1000s of gauss. This is enough to activate the hall sensor which at most requires 50 gauss.


## Issues
