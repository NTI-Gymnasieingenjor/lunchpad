# Installation

## Windows/Linux

<details>
    <summary>Follow these steps</summary><br>
  
Clone the repository:

```
git clone https://github.com/NTI-Gymnasieingenjor/lunchpad.git
```

Change working directory to lunchpad:
```
cd lunchpad
```

Install the requirements:
```
python3 -m pip install -r requirements.txt
```

Note: Replace `python3` with `python` if running on Windows.

<br>

> NOTE: If this does not work, you might need to install pip on Linux:
```
sudo apt install python3-pip
```
<br>

> NOTE: To run the program on Linux you might need to install tkinter if you don't already have it installed:

```
sudo apt-get install python3-tk
```

</details>

# Raspberry Pi Setup

### How to set up a Raspberry Pi for the lunch system

<details>
    <summary>VNC Viewer download</summary><br>
    
   VNC Viewer is an application that allows us to remotely access the Raspberry Pi.

   1. Click <a href="https://www.realvnc.com/en/connect/download/viewer/">here</a> to download VNC Viewer for your OS.
   
   2. Follow the installation guide step by step.
   
   This is all you need to do now, you will use VNC Viewer later in this setup guide.
</details>

<details>
   <summary>Enable VNC Viewer on Raspberry Pi</summary>
    
   1. Start the Raspberry Pi.
   
   2. From the desktop click the Raspberry Pi icon in the top left.
   
   3. In the drop down menu click "Preferences".
   
   4. Click "Raspberry Pi Configuration".
   
   5. In the Raspberry Pi Configuration window, click on the "Interfaces" tab.
   
   6. Make sure to enable both "SSH" and "VNC".
   
   Now you don't have to manually head into the Raspberry Pi everytime you wish to change something.
   You can just connect to the Pi via your own computer assuming you're on the same network.
</details>

<details>
    
   <summary>Connect to the Raspberry Pi</summary><br>
  
   1. In the Raspberry Pi terminal write:
   ```
   $ ifconfig
   ```
   2. Under "wlan0" you will see something like this.
   ```
   flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500<br>
   inet 10.100.100.100  netmask 000.000.0.0  broadcast 00.000.000.000
   inet6 fe80::c2ff:5f43:5cbb:eb8e  prefixlen 64  scopeid 0x20<link>
   inet6 2001:9b1:845c:201:ecdc:ec28:ce5c:89df  prefixlen 64  scopeid 0x0<g
   ```
   3. What you want to find is the "inet" ip, in the example above it's: 10.100.100.100
   
   4. Enter the inet ip you just aquired in VNC Viewer on your PC in field at the top. (Make sure you're on the same connection)
   
   5.
   
   - On a new Raspberry Pi:<br>
   Standard login credentials are:
   ```
   username: pi
   password: raspberry
   ```
   - On the old Raspberry Pi:<br>
   See "Raspberry Pi Credentials" link in README for login.
   
   6. Now you have access to the Raspberry Pi from your PC via VNC Viewer.
   
</details>

<details>
    <summary>Download Python</summary><br>
   
   Python is required to run the lunch system on the Raspberry Pi.
    
   Install Python version 3.7.2 or later on the Raspberry Pi <a href="https://www.python.org/downloads/">here.</a>

</details>
    
<details>
    
   <summary>Install Lunchpad</summary><br>
   
-  Open the terminal from the desktop.

-  Run the following command in the terminal
   ```
   $ git clone https://github.com/NTI-Gymnasieingenjor/lunchpad
   ```

   Note: If you have already ran the command above and want to update the contents of the folder. Open the terminal from the `lunchpad` folder and run the following command:
   ```
   $ git pull
   ```
   
   You now have the system on the Raspberry Pi and can run it manually whenever you want.
   
   However we don't want to restart the system manually at all. If we lose power we want it to start automatically.

</details>
  
<details>
    
   <summary>Run Lunchpad on startup</summary><br>
   
   To enable autostart on a new Raspberry Pi in case of power shutdown in any form.
   
   In the Raspberry Pi terminal write:
   ```
   $ sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
   ```
   Proceed to add these in the GNI nano 3.2 terminal.
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
   > NOTE: The filepath above "/home/pi/Desktop/lunchpad/lunchpad.py" might differ from where you add it on your own Raspberry Pi. Make sure they match.
   
</details>

<details>
   <summary>Automatic reboot at a set time</summary><br>

   In the Raspberry Pi terminal write:
   ```
   $ sudo crontab -e
   ```
   Below the comments in the terminal, add the following line below and change the stars "*" accordingly to the desired time you want a reboot.
   ```
   *    *    *    *    *  /sbin/reboot
   ```
   The following is an explanation of what the different stars mean:

   ```
   *    *    *    *    *
   ┬    ┬    ┬    ┬    ┬
   │    │    │    │    └─  Weekday  (0=Sun .. 6=Sat)
   │    │    │    └──────  Month    (1..12)
   │    │    └───────────  Day      (1..31)
   │    └────────────────  Hour     (0..23)
   └─────────────────────  Minute   (0..59)
   ```
   > NOTE: You do not need to specify all the stars, this will work perfectly for fine example:
   ```
   *    10    *    *    *  /sbin/reboot
   ```
   
    
</details>


<details>
   <summary>Turn off screens at set times</summary><br>
    
   1. In the Raspberry Pi terminal write:
   ```
   $ sudo crontab -e
   ```
   > Note: This is the same place where we set the Pi to automatically reboot at a certain time, and we'll use the same system again to turn of the screens.
   
   2. Below where we added automatic reboot in the terminal, add the following lines below and change the stars "*" accordingly to the desired time you want to turn on and off the screens.
   ```
   30 6 * * * vcgencmd display_power 1
   * 18 * * * vcgencmd display_power 0
   ```
   This will turn ON the display (display_power 1) at 6:30.<br>
   This will turn OFF the display (display_power 0) at 18:00.

   If you forgot what the stars mean refer to "Automatic reboot at a set time".
</details>

<details>
   <summary>Using two screens (Optional)</summary>
    
   1. From the desktop click the Raspberri Pi icon in the top left.
   
   3. In the drop down menu click "Preferences".
   
   4. Click "Screen Configuration".
   
   5. In this layout editor you should see HDMI 1 and HDMI 2 boxes if you have connected two screens successfully.
   
   6. Simply drag and drop one screen on top of the other to mirror it, now the displays will be mirrored.
   
</details>

# Required CSV file

For Lunchpad to function correctly, a CSV file needs to be added manually to the root folder of the program:

- *tag_time.csv*, containing a list of students and the MFR number on their keycards in this format: <br>
*class,mfr*.
- The file also includes the lunch schedule for all classes for each day of the week in this format:<br>
*class,monday,tuesday,wednesday,thursday,friday*.<br>

Times are formatted in 24 hour time with a colon between the hour and minute and a dash between the start and ending of the lunch time: *12:00-12:20*.

Below is an example of how the file can be written.

*Tags and Lunch schedule respectivly:*

```csv
1A,123123123
1A,231231231
1B,456456456
1B,465465465
1C,789789789
1C,798798798

1A_lunch,12:00-12:20,12:10-12:30,12:40-13:10,11:30-12:30,11:50-12:10
1B_lunch,11:30-11:50,11:40-12:10,12:10-12:30,11:00-11:40,11:20-11:40
1C_lunch,12:30-13:00,12:40-13:10,13:20-13:40,12:40-13:20,12:20-12:30
```

# Configure Google Services

<details>
   <summary>Google API Service Account</summary>
   
### Info

The code for Lunchpad saves the data of how many people have successfully scanned each day. For uploading this data to Google Spreadsheets, we use a Google API Service Account connected to the Raspberry Pi.

### Guide

[Here](https://docs.google.com/document/d/1Fhw4WIC9lVZuAJ3NJjE2ZAt_Lwe_UcJcmD8Hc1QBknc) is our guide on  how to create a Google API Service Account, create a key from that service account, and use that service  account key with the [gspread API](https://gspread.readthedocs.io/en/latest/index.html)

</details>

<details>
   <summary>Setup date formatting script (if new spreadsheet)</summary>
   
   1. Open spreadsheet-file in Google docs.

   2. Click on <b>Tools</b> on the toolbar.

   3. Click on <b>Script editor</b> from the list of options.

   4. Paste in the following code in the editor that opens up:
      ```javascript
      const sheetName = "Lunchsystem";

      function formatDate(range) {
        for (let i = 1; i <= range.getNumRows(); i++) {
          var cell = range.getCell(i, 1);
          var weeknum = Utilities.formatDate(new Date(cell.getValue()), "GMT+1", "w");
          cell.setNumberFormat("yyyy-mm-dd dddd v." + weeknum);
        }
      }

      function onOpen(e) {
        var sheet = e.source.getSheetByName(sheetName);
        var range = sheet.getRange("A2:A");
        formatDate(range);
      }

      function onEdit(e) {
        var sheet = e.source.getSheetByName(sheetName);
        var range = e.range;
        if (range.getColumn() == 1 && range.getRow() != 1) {
          formatDate(range);
        }
      }
      ```
      Note: Change the value of `sheetName` to the name of the sheet (<span style="color:red">Not the name of the spreadsheet</span>).

   5. Save the code.

   6. Set the name of the project. For instance, `Date formatting` and click `OK`.

</details>

<details>
   <summary>Setup time formatting script for specialcases (if new spreadsheet)</summary>
   
   1. Open spreadsheet-file in Google docs.

   2. Click on <b>Tools</b> on the toolbar.

   3. Click on <b>Script editor</b> from the list of options.

   4. Paste in the following code in the editor that opens up:
      ```javascript
        const sheetName = "Specialfall";

        function checkFormat(range) {
          let text = range.getValue();
          if (text == "" || text.match("^(2[0-3]|[0-1][0-9]):[0-5][0-9]-(2[0-3]|[0-1][0-9]):[0-5][0-9]$")) {
            range.setFontColor("black");
            range.clearNote()
          } else {
            range.setFontColor("red");
            range.setNote("Du måste skriva in i formatet: hh:mm-hh:mm Till exempel: 10:00-14:00")
          }
        }

        function onEdit(e) {
          var sheet = e.source.getSheetByName(sheetName);
          var range = e.range;
          if (range.getRow() != 1 && range.getColumn() >= 2 && range.getColumn() <= 6) {
            checkFormat(range);
          }
        }
      ```
      Note: Change the value of `sheetName` to the name of the sheet (<span style="color:red">Not the name of the spreadsheet</span>).

   5. Save the code.

   6. Set the name of the project. For instance, `Date formatting` and click `OK`.

</details>


# Usage

<details>
   <summary>lunchpad.py</summary>

   Usage:
      ```
      python3 lunchpad.py [-h] [-t [TAGS]] [-s [SCHEDULE]] [-d [DATA]]
      ```

   Scans id tags and checks if it's a person's lunchtime.
   
   | Argument                                | Help                                                                              |
   | :-------------------------------------- | :-------------------------------------------------------------------------------- |
   | -h, --help                              | Show help message and exit.                                                       |
   | -t [TAGS]     <br>--tags [TAGS]         | Specifies CSV file containing the id tags.          <br>Default: `id.csv`         |
   | -s [SCHEDULE] <br>--schedule [SCHEDULE] | Specifies CSV file containing the lunch schedule.   <br>Default: `tider.csv`      |
   | -d [DATA]     <br>--data [DATA]         | Specifies CSV file for storing the lunch data.      <br>Default: `lunch_data.csv` |

</details>

<details>
   <summary>upload_data.py</summary>

   Usage:
      ```
      python3 upload_data.py [-h] [-d [DATA]] [-w [WORKSHEET]]
      ```

   Uploads the number of people that have scanned their tags.

   | Argument                                  | Help                                                                                  |
   | :---------------------------------------- | :------------------------------------------------------------------------------------ |
   | -h<br>--help                              | Show help message and exit.                                                           |
   | -d [DATA]<br>--data [DATA]                | Specifies CSV file containing the lunch data.           <br>Default: `lunch_data.csv` |
   | -w [WORKSHEET]<br>--worksheet [WORKSHEET] | Specifies name of the worksheet on Google Spreadsheets. <br>Default: `Lunchsystem`    |
</details>

# Testing/Writing tests

## CI
All tests need to be added to the CI file located in `.github/workflow/test.yml`.
To add a new test, simply append a new test case with the correct indendation (Look at previous tests in the file) like so:
```yml
    - name: Run new test
      run: |
        python3 test_new.py
```


# In case of a Wifi shutdown

<details>
    <summary>Click here</summary>
    
### Explanation
    
The Raspberry Pi gets it's time from a <a href="https://en.wikipedia.org/wiki/Network_Time_Protocol">Network Time Protocol<a> (NTP) server from the internet via Wifi/Ethernet. <br>
If the clock is 11:00 in realtime it would be 11:00 on the Raspberry Pi.<br>

If the Raspberry Pi were to lose Wifi at 11:00 and 5 minutes pass. The time would be 11:05 both realtime and on the Raspberry Pi.<br>
This is because when it loses connection it will continue from when it lost connection, in this case 11:00.<br>

This is not a problem in itself however if the Raspberry Pi were to lose power while not connected to the Wifi, it would store the time just before shutting down.<br>
Then when it starts up again it will start from that stored time, 11:00 in this case, even if an hour has passed.<br>



### Problem

This could become a problem in the long run.

If the Raspberry Pi were to lose Wifi connection from time to time it wouldn't really matter, as the clock would continue and then reset to the correct time when it gets a connection again. <br>
However if we were to lose Wifi during a longer period of time, for example: 
* Someone accidentally turns off the Wifi and the Raspberry Pi can't automatically connect back 
* Someone accidentally disables Wifi on the Raspberry Pi
* The school decides to change something about the Wifi and the Raspberry Pi can't automatically connect back 

If any of these would happen the Raspberry Pi's time would keep running from a saved point, when it lost Wifi. 
When it then reboots everyday to clear the list, it could slip one or two minutes behind because it pasues the locally saved one. 
This could in the long run, and even after one or two weeks, pose a big problem.
One minute per day during two school weeks is 10 minutes.
This would mean that just after two weeks the class that eats 11:00 - 11:20 can't tag in and eat at 11:05 because the Raspberry Pi thinks it's 10:55.
After more weeks we would just have more problems such as classes only being able to eat 23:00 which would be horrible.

A powerdown as you can imagine would also have huge consequences, it would set the time on the Raspberry Pi back immensly. 
But only if we aren't connected to the Wifi, see "In case of a powerdown" below for more info.

### Solution

If we were to add to the Raspberry Pi a <a href="https://en.wikipedia.org/wiki/Real-time_clock">Real Time Clock</a> (RTC), we could avoid the Wifi problem entirely.

An RTC is found in your standard smartphone. It's a clock that runs from your phones battery and can be changed depending on where you are or to whatever you want.
We could add one of these to the Raspberry Pi and make it run from it's power supply. Meaning we can avoid the Wifi problem entierly.
This is beacause instead of the time being depentent from a NTP server it would just run on a local RTC which isn't dependent on Wifi.

</details>

# In case of a Powerdown

<details>
    <summary>Click here</summary>

### Currently

The system restarts automatically without any problems when the Raspberry Pi loses power. But there is a problem when it comes to the stored tags.

### Problem

We currently reset the list of used tags at the end of each day by rebooting the Raspberry Pi automatically at a set time.

The problem with this is that if it were to lose power for even just a second during lunch, the Raspberry Pi would reboot and restart the system and with that reset the list. This is problematic becasue someone might accidentally or intentionally unplug the Raspberry Pi so the list would reset.
The power might also go out randomly but that's not as likely.

In short we don't want the list to reset when the Raspberry Pi reboots, here's a solution.

### Solution

If we store the used tags in a seperate file and encrypt them there we avoid the problem entierly. <br>

This would solve the reboot problem beacuse the file wouldn't be reset when the Raspberry Pi reboots and the system restarts, instead it would be stored safely.
This also opens up possibilities such as reseting the file at a set time via a script without having to rely on the Raspberry Pi entierly.
We can also access the tags in a seperate file easier rather than in the actual code and do something else with that information. This might seem like a safety issue but since the tags will be encrypted you can't do anything with that information. 

</details>
