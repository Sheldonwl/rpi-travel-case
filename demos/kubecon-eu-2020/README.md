# KubeCon EU and Cloud-Native Con K3s Demo
The **pixel-controller** and **single-pixel** apps have been created for the *KubeCon EU and Cloud-Native Con* event on the 17th, 18th, 19th and 20th of August.  

# Apps 
## pixel-controller
Simple python application that checks if a file exists on the **/home/pi/pixels** directory in a shared volume on each node (Raspberry Pi). If the file 0 through 7 exists, the pixel-controller will enable the corresponding pixel on the Blinkt 8 LED RGB strip.  
The reason I'm using files, is because the blinkt library does not really read out what the port status is when running the **get_pixel()** function. It does work when running one single instance of the application, but does not know the status when run in different containers. This just needs a bit more research to figure out where the information is getting stored, but for the sake of this demo, this was the fastest way to get it workin. 

### pixel-controller.py
**What does it do?**  
Runs an endless loop, where it checks if any of the files names 0 through 7 are available on disk and updates the LED's accordingly.  
It's not perfect, but it gets the job done.  

**Variables:** 
- BRIGHTNESS = Give this variable a number between 0 and 255 to set the brightness of the LED's.  
- CLEAR_SLEEP = With this variable, you can adjust the sleep time in-between LED updates.  

### pixel-controller.yaml
Kubernetes DaemonSet that runs the pixel-controller app and attaches it to a volume that is shared between all **single-pixel** replicas running on the node. The *CLEAR_SLEEP* and *BRIGHTNESS* variables are also set in this manifest.

## single-pixel
Simple Python application that checks if a file between 0 and 7 exists on the attached volume and creates the next iterated number if the limit of 8 LED's has not been filled.  
  
**Variables:**  
- SLEEP = Sets the sleep interval after running the script. This is set to 9000 in the Dockerfile, to just keep running long enough for the demo. It isn't used for much else. 

### single-pixel.py
Checks if a file named 0 through 7 exists, if not, it creates the next iterated number of any existing file. 

### single-pixel.yaml
Contains a preStop command, that deletes the last created file. Meaning, if the file named 5 was created last, deleting the replica will delete that file named 5, thus removing one LED from the strip. 