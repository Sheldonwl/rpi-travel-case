FROM raspbian/stretch
 
MAINTAINER sheldonwl@not-my-real-email.com

RUN apt-get update 
RUN apt install vim git curl wget wiringpi -y
RUN apt install python3-pip python3-blinkt -y

COPY apps /home/apps

CMD ["/usr/bin/python3", "/home/apps/clear-pixels.py"] 
