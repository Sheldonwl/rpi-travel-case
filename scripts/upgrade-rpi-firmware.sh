#!/bin/bash

# The following commands are from the this tutorial: https://hackaday.com/2019/11/11/network-booting-the-pi-4/

# Update package information
sudo apt-get update

# Upgrade all packages
sudo apt-get upgrade -y

# Download the Raspberry Pi's BETA firmware
wget https://github.com/raspberrypi/rpi-eeprom/raw/master/firmware/beta/pieeprom-2020-01-17.bin

# Pull the boot config and write it to bootconf.txt
rpi-eeprom-config pieeprom-2020-01-17.bin > bootconf.txt

# Replace bootmode 0x1 with 0x21 in the bootconf.txt. This means: try SD first followed by network boot then stop.
sed -i s/0x1/0x21/g bootconf.txt

# Add the new bootconf.txt to the firmware and save it to a different binary. 
rpi-eeprom-config --out pieeprom-2020-01-17-netboot.bin --config bootconf.txt pieeprom-2020-01-17.bin

# Update the firmware with the altered .bin file. 
sudo rpi-eeprom-update -d -f ./pieeprom-2020-01-17-netboot.bin

# Check the Pi's serial and write down the last 8 characters. You will need this to setup TFTP. 
cat /proc/cpuinfo

echo "Now reboot the Pi once and AFTER the reboot, shutdown and remove the SD card. If you shutdown the Pi right after upgrading the firmware and remove the SD card, the changes won't take affect."
