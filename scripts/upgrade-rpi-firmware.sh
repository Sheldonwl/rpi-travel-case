#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y
wget https://github.com/raspberrypi/rpi-eeprom/raw/master/firmware/beta/pieeprom-2019-10-16.bin
rpi-eeprom-config pieeprom-2019-10-16.bin > bootconf.txt
sed -i s/0x1/0x21/g bootconf.txt
rpi-eeprom-config --out pieeprom-2019-10-16-netboot.bin --config bootconf.txt pieeprom-2019-10-16.bin
sudo rpi-eeprom-update -d -f ./pieeprom-2019-10-16-netboot.bin
cat /proc/cpuinfo
echo "Now reboot the Pi once and AFTER the reboot, shutdown and remove the SD card. If you shutdown the Pi right after upgrading the firmware and remove the SD card, the changes won't take affect."
