# Prepare SSD and format to ext4

## Prerequisite
- SD card flashed with chosen OS. In this example, I will be using Raspbian Buster Full. 

## Format SSD 
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