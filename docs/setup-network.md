# Setup network
Before we start using all of the Pi's we need to make some shcange to the network, so all devices had internet access. to do that we will need to execute a couple of steps. 

## Setup wlan0 and eth0
To configure wlan0 and eth0 we will need to edit the **/etc/network/interfaces** file. We will setup wlan0 to get an IP from the DHCP server in your network and set a static IP for eth0. 

```
# interfaces(5) file used by ifup(8) and ifdown(8)

# Please note that this file is written to be used with dhcpcd
# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'

# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

auto wlan0
allow-hotplug wlan0
iface wlan0 inet dhcp
  wireless-power off
  iface default inet dhcp
  wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

auto eth0
iface eth0 inet static
  address 192.168.3.10
  netmask 255.255.255.0
```  

In order to set the credentials for you WiFi use the following command: 
```
wpa_passphrase [ssid] [password]

E.g. wpa_passphrase my-home-network my-super-secret-password
```

This will generate an output like this: 
```
network={
	ssid="my-home-network"
	#psk=my-super-secret-password
	psk=d6445332c42wersdfr324sdgt35g32d2d2caa4aac458200e66dfg345fee587d9sdfrt96dc0
}

```

You can copy that output to **/etc/wpa_supplicant/wpa_supplicant.com**. 
Before you save and exit the file, remove the **#** commented out line, so you don't have your WiFi password saved in plain text in a file.  
Now you can reboot your Pi. 
```
sudo reboot
```

You can check the wireless interfaces with **iwconfig**. This is like **ifconfig**, but for wireless interfaces.
```
iwconfig
```

## Disable Power Managment 
By default the Raspberry Pi has *Power management* enabled, so you might notice your SSH sessions disconneting or your clients losing internet access. If you have used the interface file listed above, you will have also added **wireless-power off** to the wlan0 config. This will disable power management. You will need to reboot your Pi before this takes any effect. After the reboot, you can run **iwconfig** to check if it has worked. You should see an output like this: 
```
wlan0     IEEE 802.11  ESSID:"my-home-network"
          Mode:Managed  Frequency:2.412 GHz  Access Point: 5A:39:53:F7:50:A4
          Bit Rate=19.5 Mb/s   Tx-Power=31 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
-->       Power Management:off
          Link Quality=50/70  Signal level=-60 dBm
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:18  Invalid misc:0   Missed beacon:0

eth0      no wireless extensions.
```

You should see the same as at the **-->**, **Power Management:off**.

## Setup internet access for all Pi's
**Set ipv4_forward**
```
vi /etc/sysctl.conf
net.ipv4.ip_forward=1
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
```
**Configure iptables**
```
sudo iptables -t nat -A POSTROUTING -o wlan0 -j MASQUERADE
sudo iptables -A FORWARD -i wlan0 -o eth0 -m state --state RELATED
sudo iptables -A FORWARD -i eth0 -o wlan0 -j ACCEPT
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```
Save iptabbles rules by installing: 
```
sudo apt-get install iptables-persistent -y
```
During the installation you will be prompted to save your current iptables rules. Choose yes, or change it later with: 
```
sudo /etc/init.d/iptables-persistent save 
sudo /etc/init.d/iptables-persistent reload
```
If you were busy setting up the server, continue at this [step](https://github.com/Sheldonwl/rpi-travel-case/blob/master/docs/setup-server.md#setup-ssh-from-host).
