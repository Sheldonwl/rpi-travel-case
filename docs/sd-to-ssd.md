**There will eventually also be a video tutorial available here:**

# Using an SSD instead of the SD 
In this guide I will show you how to move your root file system from the SD card to a SSD drive. At the moment of writing this guide, booting of a USB storage drive is not possible with the Raspberry Pi 4. This does not mean that we can't still use the speed and reliability of a SSD. We can do this by using the SD card for the initial boot, but then point to the SSD as root file system.  

This guide contains 3 seperately usable guides, so I will split them up. This way it's also not a verty long read. :) 

### Prepare SSD and format to ext4

### Copy bootfs and rootfs from SD to SSD

### Resize SSD with data retention


# Sources:  
I had to use a couple of sources to piece this one together, but special thanks to the people that have already shared their experiences.  

Delete and format partitions (followed until step 9):  
https://www.tomshardware.com/news/boot-raspberry-pi-from-usb,39782.html  

Easy SD to SSD file copy:  
https://www.element14.com/community/community/raspberry-pi/blog/2019/08/30/quick-sd-to-ssd-on-the-pi-4  

Resize partition (Step: Reduce a Partition and Filesystem):  
https://geekpeek.net/resize-filesystem-fdisk-resize2fs/ 
