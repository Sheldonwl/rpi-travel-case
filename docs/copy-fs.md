# Copy bootfs and rootfs from SD to SSD

1. On your Raspbian desktop, go to the Raspberry icon in the top left. 
2. Open Accessories and select the **SD Card Copier** tool. 
3. From the *Copy From Device* drop down, you can select **/dev/mmcblk0** which is your SD card.
4. From the *Copy To Device* drop down, you can select your external device (/dev/sda).
5. Make sure you check the **New Partition UUIDs** box! Now click *Start*. This can take a couple of minutes. 
6. When it's done copyin, open a terminal. Type the following: 
```
sudo blkid
```
You should get an output like this: 
```
/dev/mmcblk0p1: LABEL_FATBOOT="boot" LABEL="boot" UUID="6341-C9E5" TYPE="vfat" PARTUUID="ea7d04d6-01"
/dev/mmcblk0p2: LABEL="rootfs" UUID="80571af6-21c9-48a0-9df5-cffb60cf79af" TYPE="ext4" PARTUUID="ea7d04d6-02"
/dev/sda1: LABEL_FATBOOT="boot" LABEL="boot" UUID="6341-C9E5" TYPE="vfat" PARTUUID="bfbe04bc-01"
/dev/sda2: LABEL="rootfs" UUID="80571af6-21c9-48a0-9df5-cffb60cf79af" TYPE="ext4" PARTUUID="bfbe04bc-02"
```
If you don't get this output and still only see the top 2 lines. You can restart the Pi and try again.  
When you do see the 4 lines, copy the PARTUUID of the last line. This is the PARTUUID of your root file system. In this example that's **bfbe04bc-02**.

7. Now let's change the **/boot/cmdline.txt** file, but make a backup of it first. *If you run into any issues after changing this file and the Pi won't start up. You can remove the SD card, insert it into your laptop and replace the /boot/cmdline.txt file with the backup. Insert it back into your Pi and try booting up again.*
```
sudo cp /boot/cmdline.txt /boot/cmdline.txt.bak
``` 
After backing up the file, edit the **/boot/cmdline.txt** and change the PARTUUID number. E.g.: 
Current:
```
console=serial0,115200 console=tty1 root=PARTUUID=d9b3f436-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```
After change: 
```
console=serial0,115200 console=tty1 root=PARTUUID=bfbe04bc-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
```
Of course these number will be different for you.  
Save the file and reboot the Pi. 
```
sudo reboot
```

8. After the reboot you can open up a terminal an run **df -h**. 
```
pi@master-1:~ $ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       465G   11G  269G   2% /
devtmpfs        1.9G     0  1.9G   0% /dev
tmpfs           2.0G     0  2.0G   0% /dev/shm
tmpfs           2.0G  8.7M  1.9G   1% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/sda1       253M   54M  199M  22% /boot
tmpfs           391M     0  391M   0% /run/user/1000
/dev/mmcblk0p2   29G   11G   18G  39% /media/pi/rootfs
/dev/mmcblk0p1  253M   54M  199M  22% /media/pi/boot
```
You should see that your **/dev/root** has the new size of your external drive.  
This was my old output: 
```
pi@master-1:~ $ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        29G   11G   18G  39% /
devtmpfs        1.9G     0  1.9G   0% /dev
tmpfs           2.0G     0  2.0G   0% /dev/shm
tmpfs           2.0G  8.7M  1.9G   1% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/mmcblk0p1  253M   54M  199M  22% /boot
tmpfs           391M     0  391M   0% /run/user/1000
```
As you can see, it went from 29G to 465G. Plus it's now using my SSD. :) 