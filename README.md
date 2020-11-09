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

### In Linux terminal

Clone the repository:
```
$ git clone https://github.com/NTI-Gymnasieingenjor/lunchpad.git
```

Change working directory to lunchpad:
```
$ cd lunchpad
```

Install the requirements:
```
$ python3 -m pip install -r requirements.txt
```

### In Windows terminal

Clone the repository
```
git clone https://github.com/NTI-Gymnasieingenjor/lunchpad.git
```
Change working directory to lunchpad
```
cd lunchpad
```
install the requirements
```
pip install -r requirements.txt
```

# Raspberry pi Setup

Install Python version 3.7.2 or later on the Raspberry pi:
https://www.python.org/downloads/

To enable autostart on a new Raspberry pi in case of power shutdown in any form.
```
$ sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```
Proceed to add these in the GNI nano 3.2 terminal
```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@xset s off
@xset -dpms
@xset s noblank
@sudo python3 /home/pi/Desktop/lunchpad/lunchpad.py
point-rpi
```

## Automatic reboot at a certain time

In the Raspberry pi terminal
```
$ sudo crontab -e
```
Below the comments in the terminal, add this line below <br>
and change the stars "*" accordingly to the desired time you want a reboot.

The box below the code is an explanation of what the different stars mean.
```
*    *    *    *    *  /sbin/reboot
```
```
┬    ┬    ┬    ┬    ┬
│    │    │    │    └─  Weekday  (0=Sun .. 6=Sat)
│    │    │    └──────  Month    (1..12)
│    │    └───────────  Day      (1..31)
│    └────────────────  Hour     (0..23)
└─────────────────────  Minute   (0..59)
```

# Coding Standard

**File name structure:** this_is_how_you_do (snake_case)

**Variables/Classes/Functions:** thisIsHowYouDo (camelCaseExample)

# Run on Windows

If you want to test or run the program on windows, you will have to comment out some parts of the code with a #.
The text with the # infront of it is what you will need to comment out or copy and replace.

```
    # def play_sound():
    #     global denied_sound
    #     os.system('mpg123 ' + denied_sound)
    # def start_sound():
    #     global sound_t
    #     sound_t = multiprocessing.Process(target=play_sound)
    #     sound_t.start()
```
You also need to comment out the code as shown below that resides under the "handle_enter" function. The code below occurs 3 times in the function.
```
    # start_sound()
```
```
    #root.attributes("-fullscreen", True)
```

## In case of a Wifi shutdown

#### Explanation:

The Raspberry pi gets it's time from a <a href="https://en.wikipedia.org/wiki/Network_Time_Protocol">Network Time Protocol<a> (NTP) server from the internet via Wifi/Ethernet. <br>
If the clock is 11:00 in realtime it would be 11:00 on the Raspberry pi.<br>

If the Raspberry pi were to lose Wifi at 11:00 and 5 minutes pass. The time would be 11:05 both realtime and on the Raspberry pi.<br>
This is because when it loses connection it will continue from when it lost connection, in this case 11:00.<br>

This is not a problem in itself however if the Raspberry pi were to lose power while not connected to the Wifi, it would store the time just before shutting down.<br>
Then when it starts up again it will start from that stored time, 11:00 in this case, even if an hour has passed.<br>





