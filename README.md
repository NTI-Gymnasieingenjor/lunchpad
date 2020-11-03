# Lunchpad
Lunchpad, Made by team Atlantic and team Goblins

# Definition of Done
+ Tests must pass.
+ Code must be commented.
+ No commented-out code.
+ Code and documentation must be uploaded and be up to date on GitHub.
+ Code should follow the coding conventions in place.

# Before merging with main
+ All code and documentation should be read by groupmembers onsite and approved.

# Installation

### Linux terminal
```
# Clone repository
$ git clone https://github.com/NTI-Gymnasieingenjor/lunchpad.git

# Change working directory to lunchpad
$ cd lunchpad

# install the requirements
$ python3 -m pip install -r requirements.txt
```

### Windows terminal
```
# Clone repository
git clone https://github.com/NTI-Gymnasieingenjor/lunchpad.git

# Change working directory to lunchpad
cd lunchpad

# install the requirements
pip install -r requirements.txt
```

# Raspberry pi Setup

Install Python version 3.7.2 or later on the Raspberry pi:
https://www.python.org/downloads/
```
# To enable autostart on a new Raspberry pi in case of power shutdown in any form.
$ sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

# Proceed to add these in the GNI nano 3.2 terminal

@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@xset s off
@xset -dpms
@xset s noblank
@sudo python3 /home/pi/Desktop/lunchpad/lunchpad.py
point-rpi
```
# Coding Standard
**File name structure:** this_is_how_you_do (snake_case)

**Variables/Classes/Functions:** thisIsHowYouDo (camelCaseExample)
