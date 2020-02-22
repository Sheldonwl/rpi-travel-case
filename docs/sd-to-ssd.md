**There will eventually also be a video tutorial available here:**

# Using an SSD instead of the SD 
In this guide I will show you how to move your root file system from the SD card to a SSD drive. At the moment of writing this guide, booting of a USB storage drive is not possible with the Raspberry Pi 4. This does not mean that we can't still use the speed and reliability of a SSD. We can do this by using the SD card for the initial boot, but then point to the SSD as root file system. 

# Prerequisite
- SD card flashed with chosen OS. In this example, I will be using Raspbian Buster Full. 

# Format SSD 
Before we start copying the flashed boot and root files, we'll make sure that the SSD is empty and formated to the correct file system format, ext4.  

1. Boot up Raspberry Pi.
2. Connect external drive (SSD).
3. Launch terminal. Click the terminal icon on the Desktop, type CTRL+ALT+T or SSH to the Pi from another host. 
4. Use **sudo fdisk -l** to list all drives. E.g.:
```
pi@master-1:~ $ sudo fdisk -l

Device         Boot  Start      End  Sectors  Size Id Type
/dev/mmcblk0p1        8192   532479   524288  256M  c W95 FAT32 (LBA)
/dev/mmcblk0p2      532480 62333951 61801472 29.5G 83 Linux				# This is where your data is stored


Disk /dev/sda: 465.8 GiB, 500107837440 bytes, 976773120 sectors
Disk model: Extreme SSD
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 1048576 bytes
Disklabel type: dos
Disk identifier: 0xe59694d8
```
It is important the write down the name of the external drive. In my case its **/dev/sda**, but yours might be different. 

5. Start **fdisk**, targeting your external drive. 
```
sudo fdisk /dev/sda
```
You should see the following:
```
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


Command (m for help):
```
Type **p** and hit ENTER to list the current partitions. E.g.: (The **-->** arrow will mark the locations where actions are taken or commands entered.)
```
--> Command (m for help): p
Disk /dev/sda: 465.8 GiB, 500107837440 bytes, 976773120 sectors
Disk model: Extreme SSD
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 1048576 bytes
Disklabel type: dos
Disk identifier: 0xe59694d8

Device     Boot  Start       End   Sectors   Size Id Type
/dev/sda1         8192    532479    524288   256M  c W95 FAT32 (LBA)
/dev/sda2       532480 976773119 976240640 465.5G 83 Linux
```
As you can see I have 2 partitions already there (this is not right out of the box of course). You might only have one, but that doesn't matter, we'll delete all partitions by typing **d** and hitting ENTER. 
```
--> Command (m for help): d 			# Delete partition /dev/sda2
Partition number (1,2, default 2):

Partition 2 has been deleted.

--> Command (m for help): d 			# Delete partition /dev/sda1

Partition 1 has been deleted.

--> Command (m for help): p 			# List all partitions
Disk /dev/sda: 465.8 GiB, 500107837440 bytes, 976773120 sectors
Disk model: Extreme SSD
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 1048576 bytes
Disklabel type: dos
Disk identifier: 0xe59694d8
```
As you can see, I had to delete twice. When I listed the partitions only the disc information was displayed.

6. Now let's create the new partition by typing **n** and hitting ENTER 5 times. 
```
--> Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
--> Select (default p): p 								# ENTER, the default is already p
--> Partition number (1,2,3,4, default 1): 				# ENTER, the default is already 1
--> First sector (2048-976773119, default 2048): 		# ENTER, Don't change the start sector
--> Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-976773119, default 976773119):		#ENTER, default is the last sector

Created a new partition 1 of type 'Linux' and of size 465.8 GiB.
``` 
After typing **n** you will be asked to choose between **p** (primary) and **e** (extended). The default will be **p** and that's why you could just hit ENTER. After that you are asked to choose the start and end sectors, which you don't have to manually change, so also just hit ENTER. 

7. Now let's write the changes by typing **w** and hitting ENTER. 
```
--> Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

8. Now let's format the new partition in the **ext4** file system format
```
sudo mkfs.ext4 /dev/sda1
```
This might take a couple of minutes and then were done with these steps. 

# Copy SD files to SSD 
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

# Resize SSD with data retention
**If you are doing this to a drive that already contains data you can't lose, you should first make a backup of this drive.**  

This step is only necessary if you want to use one SSD for the root file system and as a separate partition. I will be creating a 300GB root file system and use the rest for the extra partition. This requires the following steps: 
- Resize partition 
- Delete partition 
- Create new smaller partition 
- Create new extra partition 
- Format new partition to ext4


1. Check current data file system (/dev/sda) with **sudo e2fsck -f /dev/sda2**. 
```
pi@master-1:~ $ sudo e2fsck -f /dev/sda2

e2fsck 1.44.5 (15-Dec-2018)
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Pass 5: Checking group summary information
rootfs: 331911/30515200 files (0.1% non-contiguous), 5001355/122030080 blocks
```

2. Resize the file system with **sudo resize2fs /dev/sda2 300G**. This will resize my almost 500GB partition to 300GB.
```
pi@master-1:~ $ sudo resize2fs /dev/sda2 300G

resize2fs 1.44.5 (15-Dec-2018)
Resizing the filesystem on /dev/sda2 to 78643200 (4k) blocks.
The filesystem on /dev/sda2 is now 78643200 (4k) blocks long.
```

3. Now we need to delete the partition we resized. I know this seems scary, but it's not deleting any data. Where just changing the partition records. 
```
--> pi@master-1:~ $ sudo fdisk /dev/sda

Welcome to fdisk (util-linux 2.33.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


--> Command (m for help): p 		# List partitions
Disk /dev/sda: 465.8 GiB, 500107837440 bytes, 976773120 sectors
Disk model: Extreme SSD
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 1048576 bytes
Disklabel type: dos
Disk identifier: 0xe59694d8

Device     Boot  Start       End   Sectors   Size Id Type
/dev/sda1         8192    532479    524288   256M  c W95 FAT32 (LBA)
/dev/sda2       532480 976773119 976240640 465.5G 83 Linux

--> Command (m for help): d 		# Delete partition 2 (sda2)
Partition number (1,2, default 2):

Partition 2 has been deleted.

--> Command (m for help): w 		# Write changes
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

4. Now we need to create the smaller partition containing all of the data. 
```
--> pi@master-1:~ $ sudo fdisk /dev/sda

Welcome to fdisk (util-linux 2.33.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.


--> Command (m for help): p 			# List partitions
Disk /dev/sda: 465.8 GiB, 500107837440 bytes, 976773120 sectors
Disk model: Extreme SSD
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 1048576 bytes
Disklabel type: dos
Disk identifier: 0xe59694d8

Device     Boot Start    End Sectors  Size Id Type
/dev/sda1        8192 532479  524288  256M  c W95 FAT32 (LBA)

--> Command (m for help): n 			# Create new partition 
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
--> Select (default p): p 				# Choose primary type
--> Partition number (2-4, default 2): 	# Choose partition number 2 (sda2), which was the one with the data.
--> First sector (2048-976773119, default 2048): 532480		# This is important! Here we need to write the start sector, which is the End sector of sda1 +1. 
--> Last sector, +/-sectors or +/-size{K,M,G,T,P} (532480-976773119, default 976773119): +300G 		# We resized to 300G, so the partition should be that size.

Created a new partition 2 of type 'Linux' and of size 300 GiB.
Partition #2 contains a ext4 signature.

--> Do you want to remove the signature? [Y]es/[N]o: n 		# Choose NOT the remove the ext4 signature

--> Command (m for help): p 			# List partitions to check if everything is correct. 

Disk /dev/sda: 465.8 GiB, 500107837440 bytes, 976773120 sectors
Disk model: Extreme SSD
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 1048576 bytes
Disklabel type: dos
Disk identifier: 0xe59694d8

Device     Boot  Start       End   Sectors  Size Id Type
/dev/sda1         8192    532479    524288  256M  c W95 FAT32 (LBA)
/dev/sda2       532480 629678079 629145600  300G 83 Linux

--> Command (m for help): n 			# Create a new partition
Partition type
   p   primary (2 primary, 0 extended, 2 free)
   e   extended (container for logical partitions)
--> Select (default p): p 				# Choose primary type
--> Partition number (3,4, default 3): 		# Choose partition number 3
--> First sector (2048-976773119, default 2048): 629678080		# Important: choose the end sector of sda2 +1 as the start sector for sda3
--> Last sector, +/-sectors or +/-size{K,M,G,T,P} (629678080-976773119, default 976773119): 	# The last sector will by default list the last sector left over. So just hit ENTER. 

Created a new partition 3 of type 'Linux' and of size 165.5 GiB.

--> Command (m for help): p 			# List partitions
Disk /dev/sda: 465.8 GiB, 500107837440 bytes, 976773120 sectors
Disk model: Extreme SSD
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 1048576 bytes
Disklabel type: dos
Disk identifier: 0xe59694d8

console=serial0,115200 console=tty1 root=PARTUUID=e59694d8-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles
Device     Boot     Start       End   Sectors   Size Id Type
/dev/sda1            8192    532479    524288   256M  c W95 FAT32 (LBA)
/dev/sda2          532480 629678079 629145600   300G 83 Linux
/dev/sda3       629678080 976773119 347095040 165.5G 83 Linux

--> Command (m for help): w 			# Write changes
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

You can now check if the drive is available with **sudo fdisk -l**.
```
pi@master-1:~ $ sudo fdisk -l

Disk /dev/mmcblk0: 29.7 GiB, 31914983424 bytes, 62333952 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xea7d04d6

Device         Boot  Start      End  Sectors  Size Id Type
/dev/mmcblk0p1        8192   532479   524288  256M  c W95 FAT32 (LBA)
/dev/mmcblk0p2      532480 62333951 61801472 29.5G 83 Linux


Disk /dev/sda: 465.8 GiB, 500107837440 bytes, 976773120 sectors
Disk model: Extreme SSD
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 1048576 bytes
Disklabel type: dos
Disk identifier: 0xe59694d8

Device     Boot     Start       End   Sectors   Size Id Type
/dev/sda1            8192    532479    524288   256M  c W95 FAT32 (LBA)
/dev/sda2          532480 629678079 629145600   300G 83 Linux
/dev/sda3       629678080 976773119 347095040 165.5G 83 Linux
```
As you can see, I now have a 300G root file system (/dev/sda2) and and extra 165.5G (/dev/sda3) partition. 

5. Before we can start using the extra partition we need to format it correctly, or else you might see the following when doing a check: 
```
pi@master-1:~ $ sudo e2fsck -f /dev/sda3

e2fsck 1.44.5 (15-Dec-2018)
ext2fs_open2: Bad magic number in super-block
e2fsck: Superblock invalid, trying backup blocks...
Superblock has an invalid journal (inode 8).
Clear<y>? cancelled!
e2fsck: The journal superblock is corrupt while checking journal for rootfs
e2fsck: Cannot proceed with file system check

rootfs: ***** FILE SYSTEM WAS MODIFIED *****

rootfs: ********** WARNING: Filesystem still has errors **********
```

No worries, we just need to format it with **sudo mkfs.ext4 /dev/sda3**: 
```
pi@master-1:~ $ sudo mkfs.ext4 /dev/sda3

mke2fs 1.44.5 (15-Dec-2018)
Discarding device blocks: done
Creating filesystem with 43386880 4k blocks and 10854400 inodes
Filesystem UUID: 39ce9595-d79a-4d6c-a9ef-8f3f990d2538
Superblock backups stored on blocks:
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
	4096000, 7962624, 11239424, 20480000, 23887872

Allocating group tables: done
Writing inode tables: done
Creating journal (262144 blocks): done
Writing superblocks and filesystem accounting information: done
```

Let's check again: 
```
pi@master-1:~ $ sudo e2fsck -f /dev/sda3

e2fsck 1.44.5 (15-Dec-2018)
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Pass 5: Checking group summary information
/dev/sda3: 11/10854400 files (0.0% non-contiguous), 958891/43386880 blocks
```
All fixed! Now all you need to do is mount it. For example, like this: 
```
pi@master-1:~ $ sudo mkdir /persistent_storage
pi@master-1:~ $ sudo mount /dev/sda3 /persistent_storage
pi@master-1:~ $ df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       295G   11G  269G   4% /
devtmpfs        1.9G     0  1.9G   0% /dev
tmpfs           2.0G     0  2.0G   0% /dev/shm
tmpfs           2.0G  8.7M  1.9G   1% /run
tmpfs           5.0M  4.0K  5.0M   1% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/sda1       253M   54M  199M  22% /boot
tmpfs           391M     0  391M   0% /run/user/1000
/dev/mmcblk0p2   29G   11G   18G  39% /media/pi/rootfs
/dev/mmcblk0p1  253M   54M  199M  22% /media/pi/boot
/dev/sda3       162G   61M  154G   1% /persistent_storage
```
As you can see, we have created the */persistent_storage* directory and have mounted */dev/sda3* to it.  
Well, that's it! We've resized the already existing sda2 partition to 300GB. After which, we've created a new partition with the rest of the available memory. 

# Sources:  
I had to use a couple of sources to piece this one together, but special thanks to the people that have already shared their experiences.  

Delete and format partitions (followed until step 9:  
https://www.tomshardware.com/news/boot-raspberry-pi-from-usb,39782.html  


Easy SD to SSD file copy:  
https://www.element14.com/community/community/raspberry-pi/blog/2019/08/30/quick-sd-to-ssd-on-the-pi-4  

Resize partition:  
https://geekpeek.net/resize-filesystem-fdisk-resize2fs/ 
