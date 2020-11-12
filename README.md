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

# Coding Standard

**File name structure:** this_is_how_you_do (snake_case)

**Variables/Classes/Functions:** thisIsHowYouDo (camelCaseExample)


# Installation

## In Linux Terminal

<details>
    <summary>Follow these steps</summary><br>
  
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
</details>

## In Windows Terminal

<details>
    <summary>Follow these steps</summary><br>

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
</details>



# Raspberry pi Setup

### How to set up a Raspberry pi for the lunch system

<details>
    <summary>VNC Viewer download</summary><br>
    
   VNC Viewer is an application that allows us to remotley access the raspberry pi.

   1. Click <a href="https://www.realvnc.com/en/connect/download/viewer/">here</a> to download VNC Viewer for your OS.
   
   2. Follow the installation guide step by step
   
   This is all you need to do now, you will use VNC Viewer later in this setup guide.
</details>

<details>
   <summary>Enable VNC Viewer on Raspberry pi</summary>
    
   1. Start the Raspberry pi
   
   2. From the desktop click the Raspberri pi icon in the top left
   
   3. In the drop down menu click "Preferences"
   
   4. Click "Raspberry Pi Configuration"
   
   5. In the Raspberry Pi Configuration window, click on the "Interfaces" tab
   
   6. Make sure to enable both "SSH" and "VNC"
   
   Now you don't have to manually head into the Raspberry pi everytime you wish to change something.
   You can just connect to the pi via your own computer assuming you're on the same network.
</details>

<details>
    
   <summary>Connect to the Raspberry pi</summary><br>
   
   1. In the Raspberry pi terminal write
   ```
   $ ifconfig
   ```
   2. Under "wlan0" you will see something like this
   ```
   flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500<br>
   inet 10.100.100.100  netmask 000.000.0.0  broadcast 00.000.000.000
   inet6 fe80::c2ff:5f43:5cbb:eb8e  prefixlen 64  scopeid 0x20<link>
   inet6 2001:9b1:845c:201:ecdc:ec28:ce5c:89df  prefixlen 64  scopeid 0x0<g
   ```
   3. What you want to find is the "inet" ip, in the example above it's: 10.100.100.100
   
   4. Enter the inet ip you just aquired in VNC Viewer on your PC in field at the top. (Make sure you're on the same connection)
   
   5. Standard login credentials are:
   ```
   username: pi
   password: raspberry
   ```
   6. Now you have access to the Raspberry pi from your PC.
</details>

<details>
    <summary>Download Python</summary><br>
   
   When we have the sytem on the Raspberry pi we need Python to actually run it.
    
   Install Python version 3.7.2 or later on the Raspberry pi <a href="https://www.python.org/downloads/">here</a>

</details>
    
<details>
    
   <summary>Upload lunch system folder to Raspberry pi</summary><br>
   
   - Click and drag the "lunchpad" folder you cloned over to the Raspberry pi desktop window
   
   You now have the system on the Raspberry pi and can run it manually whenever you want.
   
   However we don't want to restart the system manually at all. If we lose power we want it to start automatically.
   
</details>
  
<details>
    
   <summary>Enable autostart on raspberry pi</summary><br>
   
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
   > NOTE: The filepath above "/home/pi/Desktop/lunchpad/lunchpad.py" might differ from where you add it on your own Raspberry pi. Make sure they match.
   
</details>

<details>
   <summary>Automatic reboot at a set time</summary><br>

   In the Raspberry pi terminal
   ```
   $ sudo crontab -e
   ```
   Below the comments in the terminal, add the line below and change the stars "*" accordingly to the desired time you want a reboot.
   ```
   *    *    *    *    *  /sbin/reboot
   ```
   This is an explanation of what the different stars mean.

   ```
   *    *    *    *    *
   ┬    ┬    ┬    ┬    ┬
   │    │    │    │    └─  Weekday  (0=Sun .. 6=Sat)
   │    │    │    └──────  Month    (1..12)
   │    │    └───────────  Day      (1..31)
   │    └────────────────  Hour     (0..23)
   └─────────────────────  Minute   (0..59)
   ```
    
</details>


<details>
   <summary>Turn off screens at set times</summary><br>
    
   1. In the Raspberry pi terminal
   ```
   $ sudo crontab -e
   ```
   > Note: This is the same place where we set the pi to automatically reboot at a certain time, and we'll use the same system again to turn of the screens.
   
   2. Below where we added automatic reboot in the terminal, add the lines below and change the stars "*" accordingly to the desired time you want to turn on and off the screens.
   ```
   30 6 * * * vcgencmd display_power 1
   * 18 * * * vcgencmd display_power 0
   ```
   This will turn ON the display (display_power 1) at 6:30.<br>
   This will turn OFF the display (display_power 0) at 18:00.

   If you forgot what the stars mean see "Automatic reboot at a set time".
</details>

<details>
   <summary>Using two screens (Optional)</summary>
    
   1. From the desktop click the Raspberri pi icon in the top left
   
   3. In the drop down menu click "Preferences"
   
   4. Click "Screen Configuration"
   
   5. In this layout editor you should see HDMI 1 and HDMI 2 boxes if you have connected two screns successfully
   
   6. Simply drag and drop one screen on the other to mirror it, now it will display the same thing on both screens
   
</details>

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

# In case of a Wifi shutdown

### Explanation

The Raspberry pi gets it's time from a <a href="https://en.wikipedia.org/wiki/Network_Time_Protocol">Network Time Protocol<a> (NTP) server from the internet via Wifi/Ethernet. <br>
If the clock is 11:00 in realtime it would be 11:00 on the Raspberry pi.<br>

If the Raspberry pi were to lose Wifi at 11:00 and 5 minutes pass. The time would be 11:05 both realtime and on the Raspberry pi.<br>
This is because when it loses connection it will continue from when it lost connection, in this case 11:00.<br>

This is not a problem in itself however if the Raspberry pi were to lose power while not connected to the Wifi, it would store the time just before shutting down.<br>
Then when it starts up again it will start from that stored time, 11:00 in this case, even if an hour has passed.<br>

### Problem

This could become a problem in the long run.

If the Raspberry pi were to lose Wifi connection from time to time it wouldn't really matter, as the clock would continue and then reset to the correct time when it gets a connection again. <br>
However if we were to lose Wifi during a longer period of time, for example: 
* Someone accidentally turns off the Wifi and the Raspberry pi can't automatically connect back 
* Someone accidentally disables Wifi on the Raspberry pi
* The school decides to change something about the Wifi and the Raspberry pi can't automatically connect back 

If any of these would happen the Raspberry pi's time would keep running from a saved point, when it lost Wifi. 
When it then reboots everyday to clear the list, it could slip one or two minutes behind because it pasues the locally saved one. 
This could in the long run, and even after one or two weeks, pose a big problem.
One minute per day during two school weeks is 10 minutes.
This would mean that just after two weeks the class that eats 11:00 - 11:20 can't tag in and eat at 11:05 because the Raspberry pi thinks it's 10:55.
After more weeks we would just have more problems such as classes only being able to eat 23:00 which would be horrible.

A powerdown as you can imagine would also have huge consequences, it would set the time on the Raspberry pi back immensly. 
But only if we aren't connected to the Wifi, see "In case of a powerdown" below for more info.

### Solution

If we were to add to the Raspberry pi a <a href="https://en.wikipedia.org/wiki/Real-time_clock">Real Time Clock</a> (RTC), we could avoid the Wifi problem entirely.

An RTC is found in your standard smartphone. It's a clock that runs from your phones battery and can be changed depending on where you are or to whatever you want.
We could add one of these to the Raspberry pi and make it run from it's power supply. Meaning we can avoid the Wifi problem entierly.
This is beacause instead of the time being depentent from a NTP server it would just run on a local RTC which isn't dependent on Wifi.

# In case of a Powerdown

### Currently

The system restarts automatically without any problems when the Raspberry pi loses power. But there is a problem when it comes to the stored tags.

### Problem

We currently reset the list of used tags at the end of each day by rebooting the Raspberry pi automatically at a set time.

The problem with this is that if it were to lose power for even just a second during lunch, the Raspberry pi would reboot and restart the system and with that reset the list. This is problematic becasue someone might accidentally or intentionally unplug the Raspberry pi so the list would reset.
The power might also go out randomly but that's not as likely.

In short we don't want the list to reset when the Raspberry pi reboots, here's a solution.

### Solution

If we store the used tags in a seperate file and encrypt them there we avoid the problem entierly. <br>

This would solve the reboot problem beacuse the file wouldn't be reset when the Raspberry pi reboots and the system restarts, instead it would be stored safely.
This also opens up possibilities such as reseting the file at a set time via a script without having to rely on the Raspberry pi entierly.
We can also access the tags in a seperate file easier rather than in the actual code and do something else with that information. This might seem like a safety issue but since the tags will be encrypted you can't do anything with that information. 




