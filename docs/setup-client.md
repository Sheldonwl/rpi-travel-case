# Setup Client
We will be network booting the clients, but need to upgrade the Raspberry Pi's SPI EEPROM Bootloader before we can do that. At the time of creation	this feature is still in BETA, so we need to flash the BETA firmware to the client Pi. 

## Prerequisites 
- SD card flashed with Raspbian full or lite
- Internet access 

## Upgrade firmware
With the following commands you will install git and access a script that will do the firmware upgrade for you. 
```
sudo apt update
sudo apt install git -y
git clone https://github.com/Sheldonwl/rpi-travel-case/
source rpi-travel-case/scripts/upgrade-rpi-firmware.sh
```
The final output will be from **cat /proc/cpuinfo** in the script. This prints out information about the Pi. Write down the last 8 characters of the Pi's serial number, as we will need that for the TFTP directories. 
After running the upgrade script, reboot the Pi (**sudo reboot**). After the reboot, you can check the bootloader config with: 
```
vcgencmd bootloader_config
```
It is also recommended to disable the auto update feature for the firmware, or else it might get overwritten. 
```
sudo systemctl mask rpi-eeprom-update
```
Now you can shutdown the Pi and remove the SD card.  

The steps listed above can be done by starting from scratch for every client, but you can also use the same SD card for multiple Pi's. The most import thing is that the BETA firmware gets downloaded ones and can afterwards be re-applied to multiple Pi's.
