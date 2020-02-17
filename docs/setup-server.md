# Setup Server

## Prerequisites 
- SD card flashed with Raspbian full or lite (Do not insert into Pi after flashing)

## Configure Waveshare TFT-LCD Touchscreen
Before we insert the newly flashed SD card in the Pi, we will first edit the **config.txt** file on the SD card. Add the following to the config: 
```
max_usb_current=1
hdmi_group=2
hdmi_mode=87
hdmi_cvt 1024 600 60 6 0 0 0
hdmi_drive=1
```

We also need to comment out or remove: **dtoverlay=vc4-fkms-v3d**  
You can check if this is still needed by going to the info page for this screen. https://www.waveshare.com/wiki/7inch_HDMI_LCD_(C)
Now insert the SD card (in a powered off Pi) and connect the power. 

## Setup Pi
Ones the Pi has booted up, you will see the Desktop (if the full image is used).  
Go through the default settings. Country/Language etc. Change password. Enable WiFi.  
Before restarting go to Preferences -> Raspberry Pi Configuration -> Interfaces -> and enable ssh.  
Now reboot your Pi.
```
sudo reboot
```

## Set static IP for eth0
Source: https://raspberrypi.stackexchange.com/questions/37920/how-do-i-set-up-networking-wifi-static-ip-address/74428#74428  

Install vim package (or any other text editor)
```
apt-get install vim -y 
```

Add this to **/etc/dhcpcd.conf**:
```
interface eth0
static ip_address=192.168.3.10/24
static routers=192.168.3.1
static domain_name_servers=192.168.3.1
```
Of course you can use any IP range you like.
Now reboot your Pi. 
```
sudo reboot
```
You will need to enable WiFi (if you haven't already) so we can SSH into the Pi. 

## Setup SSH from host
Let's copy your public key to the Raspberry Pi. To copy your public key to your Raspberry Pi, use the following command to append the public key to your authorized_keys file on the Pi, sending it over SSH:
```
ssh-copy-id <USERNAME>@<IP-ADDRESS>
E.g. ssh-copy-id pi@192.168.3.10
```
If you don't have an SSH key yet, you can create one like this: 
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
# Just keep pressing ENTER, the defaults are usually fine. 
# Now let's copy the key to the Pi.
ssh-copy-id <USERNAME>@<IP-ADDRESS>
```

## Setup file system (per client) - NFS & TFTP
The following commands are exactly what I used to create the file systems for 5 client Pi's. I used the Raspbian Lite image as the base. If you create less clients, just leave out the ones you don't need and change the names if you'd like. I chose to create a file system per client, because I want them to have and keep their own hostnames, configs, files, etc. You don't have to, but then the clients will share the same file system. If it gets corrupted, you lose all clients. 

```
# Install necessary packages.
sudo apt-get install unzip kpartx dnsmasq nfs-kernel-server -y

# Create file location for the image. Download the Lite image and create device mapper entries. 
mkdir -p ~/boot-images/lite
cd ~/boot-images/lite
wget https://downloads.raspberrypi.org/raspbian_lite_latest
unzip raspbian_lite_latest
sudo kpartx -a -v [extracted-file].img

mkdir rootmnt
mkdir bootmnt
sudo mount /dev/mapper/loop0p2 rootmnt/
sudo mount /dev/mapper/loop0p1 bootmnt/

# Create NFS directories for all clients.
sudo mkdir -p /nfs/worker-{1..3} /nfs/master-{2..3}

# Copy the rootmnt and bootmnt mounted files to all of my client directories.
sudo cp -a rootmnt/* /nfs/master-2/
sudo cp -a rootmnt/* /nfs/master-3/
sudo cp -a rootmnt/* /nfs/worker-1/
sudo cp -a rootmnt/* /nfs/worker-2/
sudo cp -a rootmnt/* /nfs/worker-3/

sudo cp -a bootmnt/* /nfs/master-2/boot/
sudo cp -a bootmnt/* /nfs/master-3/boot/
sudo cp -a bootmnt/* /nfs/worker-1/boot/
sudo cp -a bootmnt/* /nfs/worker-2/boot/
sudo cp -a bootmnt/* /nfs/worker-3/boot/

# Remove default start4.elf and fixup4.dat files
sudo rm /nfs/master-2/boot/start4.elf
sudo rm /nfs/master-2/boot/fixup4.dat
sudo rm /nfs/master-3/boot/start4.elf
sudo rm /nfs/master-3/boot/fixup4.dat
sudo rm /nfs/worker-1/boot/start4.elf
sudo rm /nfs/worker-1/boot/fixup4.dat
sudo rm /nfs/worker-2/boot/start4.elf
sudo rm /nfs/worker-2/boot/fixup4.dat
sudo rm /nfs/worker-3/boot/start4.elf
sudo rm /nfs/worker-3/boot/fixup4.dat

# Create directories and download updated start4.elf and fixup4.dat
mkdir ~/boot-images/firmware
cd ~/boot-images/firmware

sudo wget https://github.com/Hexxeh/rpi-firmware/raw/master/start4.elf
sudo wget https://github.com/Hexxeh/rpi-firmware/raw/master/fixup4.dat

sudo cp -a start4.elf /nfs/master-2/boot/start4.elf
sudo cp -a fixup4.dat /nfs/master-2/boot/fixup4.dat
sudo cp -a start4.elf /nfs/master-3/boot/start4.elf
sudo cp -a fixup4.dat /nfs/master-3/boot/fixup4.dat
sudo cp -a start4.elf /nfs/worker-1/boot/start4.elf
sudo cp -a fixup4.dat /nfs/worker-1/boot/fixup4.dat
sudo cp -a start4.elf /nfs/worker-2/boot/start4.elf
sudo cp -a fixup4.dat /nfs/worker-2/boot/fixup4.dat
sudo cp -a start4.elf /nfs/worker-3/boot/start4.elf
sudo cp -a fixup4.dat /nfs/worker-3/boot/fixup4.dat

```

During the creation of the clients you wrote down the 8 characters of the clients serial number. This is where we will use that information. 
Now let's setup the directories. You will need to change the serial numbers	to match yours. 

```
# Create directories
sudo mkdir -p /tftpboot/{6803f1db,909c57f7,7ec3392a,1227aeb4,228985e3}

# Setup bind mount so the /boot folder is accessible as part of the tftp service, as well as being mounted as part of the NFS share. The advantage here is that the kernel and rest of the boot code can be updated using apt.

echo "/nfs/master-2/boot /tftpboot/6803f1db none defaults,bind 0 0" | sudo tee -a /etc/fstab
echo "/nfs/master-3/boot /tftpboot/909c57f7 none defaults,bind 0 0" | sudo tee -a /etc/fstab
echo "/nfs/worker-1/boot /tftpboot/7ec3392a none defaults,bind 0 0" | sudo tee -a /etc/fstab
echo "/nfs/worker-2/boot /tftpboot/1227aeb4 none defaults,bind 0 0" | sudo tee -a /etc/fstab
echo "/nfs/worker-3/boot /tftpboot/228985e3 none defaults,bind 0 0" | sudo tee -a /etc/fstab

sudo mount /tftpboot/6803f1db
sudo mount /tftpboot/909c57f7
sudo mount /tftpboot/7ec3392a
sudo mount /tftpboot/1227aeb4
sudo mount /tftpboot/228985e3

sudo chmod 777 /tftpboot

# Add empty ssh file to the boot directory, so SSH is enabled by default. We will need to access the clients without attaching any peripherals of course. 
sudo touch /nfs/master-2/boot/ssh
sudo touch /nfs/master-3/boot/ssh
sudo touch /nfs/worker-1/boot/ssh
sudo touch /nfs/worker-2/boot/ssh
sudo touch /nfs/worker-3/boot/ssh

# Modify the Pi’s fstab so it won’t look for filesystems on the SD card
sudo sed -i /UUID/d /nfs/master-2/etc/fstab
sudo sed -i /UUID/d /nfs/master-3/etc/fstab
sudo sed -i /UUID/d /nfs/worker-1/etc/fstab
sudo sed -i /UUID/d /nfs/worker-2/etc/fstab
sudo sed -i /UUID/d /nfs/worker-3/etc/fstab

# Replace the boot command in cmdline.txt (be sure to replace nfsroot IP address with the IP of the Debian machine serving as the PXE server)
echo "console=serial0,115200 console=tty root=/dev/nfs nfsroot=192.168.3.10:/nfs/master-2,vers=3 rw ip=dhcp rootwait elevator=deadline" | sudo tee /nfs/master-2/boot/cmdline.txt
echo "console=serial0,115200 console=tty root=/dev/nfs nfsroot=192.168.3.10:/nfs/master-3,vers=3 rw ip=dhcp rootwait elevator=deadline" | sudo tee /nfs/master-3/boot/cmdline.txt
echo "console=serial0,115200 console=tty root=/dev/nfs nfsroot=192.168.3.10:/nfs/worker-1,vers=3 rw ip=dhcp rootwait elevator=deadline" | sudo tee /nfs/worker-1/boot/cmdline.txt
echo "console=serial0,115200 console=tty root=/dev/nfs nfsroot=192.168.3.10:/nfs/worker-2,vers=3 rw ip=dhcp rootwait elevator=deadline" | sudo tee /nfs/worker-2/boot/cmdline.txt
echo "console=serial0,115200 console=tty root=/dev/nfs nfsroot=192.168.3.10:/nfs/worker-3,vers=3 rw ip=dhcp rootwait elevator=deadline" | sudo tee /nfs/worker-3/boot/cmdline.txt
```

The NFS share is setup by adding a line to **/etc/exports** and starting the service.
```
echo "/nfs/master-2 *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports
echo "/nfs/master-3 *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports
echo "/nfs/worker-1 *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports
echo "/nfs/worker-2 *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports
echo "/nfs/worker-3 *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports

sudo systemctl enable rpcbind
sudo systemctl enable nfs-kernel-server
sudo systemctl restart rpcbind
sudo systemctl restart nfs-kernel-server
```

## Setup dnsmasq
Let's backup the original **/etc/dnsmasq.conf**: 
```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bak
```

Create and add the following to **/etc/dnsmasq.conf**:
(*dhcp-host=dc:a6:32:72:39:78,192.168.3.11,1h # master-2*: I am creating static IP's for the Pi's, but those are linked to their MAC address, so you will need to remove those lines or add you own MAC addresses) 

```
no-resolv
interface=eth0
dhcp-authoritative
domain=k3s.cluster
dhcp-range=192.168.3.11,192.168.3.21,1h
dhcp-host=dc:a6:32:72:39:78,192.168.3.11,1h # master-2
dhcp-host=dc:a6:31:72:35:62,192.168.3.12,1h # master-3
dhcp-host=dc:a6:34:72:39:71,192.168.3.13,1h # worker-1
dhcp-host=dc:a6:32:72:35:52,192.168.3.14,1h # worker-2
dhcp-host=dc:a6:32:72:39:74,192.168.3.15,1h # worker-3
dhcp-lease-max=10
log-dhcp
enable-tftp
tftp-root=/tftpboot
pxe-service=0,"Raspberry Pi Boot"
```
Restart dnsmasq and anable the service. 
```
sudo systemctl restart dnsmasq.service
sudo systemctl enable dnsmasq
```

You can see the dnsmasq logs by using either of these commands:
```
sudo tail -f /var/log/daemon.log
tail -f /var/log/syslog
```

# Backup SD card 
##Mac
Backup:
```
diskutil list
sudo dd if=/dev/disk of=~/SDCardBackup.dmg
```
Restore:
```
diskutil unmountDisk /dev/disk1
sudo dd if=~/SDCardBackup.dmg of=/dev/disk1
sudo diskutil eject /dev/rdisk3
```
# Helpful links
http://www.raspibo.org/wiki/index.php?title=Raspberry_PI:_network_boot_explained  
https://hackaday.com/2019/11/11/network-booting-the-pi-4/  
https://linuxhit.com/raspberry-pi-pxe-boot-netbooting-a-pi-4-without-an-sd-card/  
https://thepihut.com/blogs/raspberry-pi-tutorials/17789160-backing-up-and-restoring-your-raspberry-pis-sd-card
