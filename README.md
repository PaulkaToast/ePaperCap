# e-Paper Graduation Cap

Mortar board with e-paper display which is controllable through bluetooth.

<img src="https://i.imgur.com/x0o6L6U.jpg" width="500"/>

## Hardware
- [7.5inch e-Paper HAT (C)](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B))
- [Raspberry Pi 3 B](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)

## Contents
**image_process.ipynb** : This is a python jupyter notebook script to assist in converting images into the format expected by the e-paper display.

**<div style="display: inline">grad.py</div>** : This is the python script that runs on the pi to drive the display and recieve input via bluetooth.

## Setup

On your raspberry pi download the driver for the e-paper display from waveshare and follow their README instructions [here](https://github.com/waveshare/e-Paper/tree/master/7.5inch_e-paper_b%26c_code/RaspberryPi/python2)

In addition you will need to set up bluetooth communication, I used the begining of this [tutorial](https://circuitdigest.com/microcontroller-projects/controlling-raspberry-pi-gpio-using-android-app-over-bluetooth) to set it up but the TL:DR is:

First: install the packages needed

```
sudo apt-get install bluetooth blueman bluez
sudo apt-get install python-bluetooth
```

Second: pair your mobile device 
```
sudo bluetoothctl
```
```
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# discoverable on
[bluetooth]# pairable on
[bluetooth]# scan on
```
```
pair <mac address of your phone>
```

In addition you'll need a way to communicate to the pu via bluetooth. I found that bluetooth terminal apps for your smart phone a very easy way to do this.