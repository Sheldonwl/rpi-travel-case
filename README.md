# rpi-travel-case

```
Some important notes about Rancher/K3s: 

1. The Rancher management server does not run on armv7. It will run on a 64 bit architecture. 
2. You can import K3s clusters into an external Rancher, but the Rancher server components do not run on armv7, as that is 32 bit. The latest Raspberry Pi's actually have 64 bit hardware, but the Raspbian Buster image is 32 bit. So, as long as you put a 64 bit OS on the Pi, you can import that K3s cluster into an external Rancher management server. 
```


This repository contains all info needed to recreate my Raspberry Pi Travel Case. This travel case was created to demo K3s and consists of 6 Raspberry Pi 4B's, a 7" Touchscreen, 500GB SSD and Pimodori Blinkt RGB LED's. The setup consists of a Server and 5 clients. With PXE boot the clients netboot of the server.  
You can find a full video tutorial on how to make this here: https://youtu.be/_AeoSeVzzSM

For more info on K3s, checkout: https://k3s.io  

### Shopping list
Go to: [Shopping list](https://github.com/Sheldonwl/rpi-travel-case/blob/master/docs/shopping-list.md)  

### Setup Client
Go to: [Setup Client](https://github.com/Sheldonwl/rpi-travel-case/blob/master/docs/setup-client.md)  

### Setup Server 
Go to: [Setup Server](https://github.com/Sheldonwl/rpi-travel-case/blob/master/docs/setup-server.md)  

### Setup Network
Go to: [Setup network](https://github.com/Sheldonwl/rpi-travel-case/blob/master/docs/setup-network.md)

### Use SSD instead of SD
Go to: [SD to SSD](https://github.com/Sheldonwl/rpi-travel-case/blob/master/docs/sd-to-ssd.md)

### Setup K3s
Go to: [Setup K3s](https://github.com/Sheldonwl/rpi-travel-case/blob/master/docs/setup-k3s.md)

### Hardware
Go to: [Hardware](https://github.com/Sheldonwl/rpi-travel-case/blob/master/docs/hardware.md)






![Alt text](/docs/images/2.jpg?raw=true "Raspberry Pi Travel Case Cluster")
![Alt text](/docs/images/1.jpg?raw=true "Raspberry Pi Travel Case Cluster")




 
