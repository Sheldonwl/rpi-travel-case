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
--> Select (default p): p 			# Choose primary type
--> Partition number (2-4, default 2): 	# Choose partition number 2 (sda2), which was the one with the data.
--> First sector (2048-976773119, default 2048): 532480		# This is important! Here we need to write the start sector, which is the End sector of sda1 +1. 
--> Last sector, +/-sectors or +/-size{K,M,G,T,P} (532480-976773119, default 976773119): +300G		# We resized to 300G, so the partition should be that size.

Created a new partition 2 of type 'Linux' and of size 300 GiB.
Partition #2 contains a ext4 signature.

--> Do you want to remove the signature? [Y]es/[N]o: n		# Choose NOT the remove the ext4 signature

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
--> Select (default p): p 			# Choose primary type
--> Partition number (3,4, default 3): 		# Choose partition number 3
--> First sector (2048-976773119, default 2048): 629678080	# Important: choose the end sector of sda2 +1 as the start sector for sda3
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
