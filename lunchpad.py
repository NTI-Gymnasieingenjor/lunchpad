#!/usr/bin/env python3
import datetime
import time
import turtle
import threading
import sys, os
import os.path
import multiprocessing
import hashlib
import platform

def get_file_data(filepath, mode="tags"):
    """ 
    Reads respective csv file and adds the content into a list.

    Reads the csv file. Reads line by line, removing the "," and appends every item to the list, "data".
    """
    data = []
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            line_data = line.rstrip().split(",")
            data.append(line_data)
            line = fp.readline()
    return data

def find_matching_tag(tag, tags):
    """ 
    Looks through all the tags and returns the tag and its corresponding class, otherwise it returns an empty list
    """
    match = list(filter(lambda x: tag in x, tags))
    if(len(match) > 0):
        return match[0]
    else:
        return match

def find_matching_lunch_time(grade, times):
    """ 
    Uses the class of a corresponding tag to find the matching lunch times, then returns the corresponding lunch times.
    """
    match = list(filter(lambda x: grade in x, times))
    if(len(match) > 0):
        return match[0]
    else:
        return match

# Takes a time value, for example 12:00 and splits it,
# then converts it into minutes
def get_time_in_min(timestamp):
    """ 
    Takes a timestamp, for example 12:00 and splits it, then converts it into minutes.

    Takes the lunch times that "find_matching_lunch_time" finds. Splits the minutes from the hours, for example 12:30 into 12 and 30. 
    Converts the hours into minutes, for example 12 hours into 720 minutes. After that it adds the minutes and the converted hours and gets a total value of minutes.
    The time then gets returned as "total_minutes"
    """
    hours, minutes = timestamp.split(":")
    total_minutes = int(hours)*60+int(minutes)
    return total_minutes


def write_text_turtle(window, turtle, style, granted, msg=""):
    """ 
    If granted is true, turtle will make the ui-background green. Else, if granted is not true, the ui-background will turn red.
    """
    turtle.write(msg, font=style, align='center')
    if(granted):
        window.bgcolor("green")
    else:
        window.bgcolor("red")
    blipp_your_tagg()

    
# Default display
def blipp_your_tagg():
    global timer
    global style

    def _timeout():
        """ 
        Default screen for the ui

        Clears the current screen. Writes out the text saved in the "skanna_tagg" variable in the center of the screen. 
        Also sets the ui-background to black. This is done 3 seconds after a tag is scanned.
        """
        global timer
        turtle.clear()
        turtle.write(skanna_tagg, font=style, align='center')
        turtle.bgcolor("black")
        timer = None

    timer = threading.Timer(3.0, _timeout)
    timer.start()


def handle_enter(window, style):
    """ 
    Kills the sound and resets the timer if a new tag is entered before the ui-background has reset into its normal state.
    
    Creates a list where all key presses are stored. The key presses are joined together and stored in a variable called mfr.

    "allowed" and "message" recives it's values from the respective returns in the "handle_input" function.
    The function then writes the recieved message on the screen using the "write_text_turtle" function.
    If allowed is returned as false, the function "start_sound" is called.
    """
    global timer, sound_t, file
    if timer:
        timer.cancel()
    if sound_t and sound_t.is_alive():
        sound_t.terminate()

    turtle.clear()

    # "mfr" variable refers to the MFR ID,
    # Displayed on the back of the tag
    global key_presses
    mfr = "".join(key_presses)
    key_presses = []
    allowed, message = handle_input(mfr, tags_root, times_root, datetime.datetime.now(), used_tags, data_file)
    write_text_turtle(window, turtle, style, allowed, message)
    print(message)
    if allowed == False:
        start_sound()

def save_students_eaten(date,school,filename):
    """ Saves the students eaten data to lunch_data.csv 
    
    <><><><><><><><><><><><><> JaG bEhÖvEr HjÄlP mEd AtT kOmMeNtErA dEn HäR dElEn Av KoDeN <><><><><><><><><><><><><>

    """

    date = date.strftime('%Y-%m-%d')

    try:
        with open(filename, "r+") as fp:
            lunch_data = fp.readlines()
            modified = False
            for idx, line in enumerate(lunch_data):
                line = line.replace('\x00', '')
                lunch_data[idx] = line
                if date in line:
                    modified = True
                    new_line = line.split(",")
                    if school == "NTI":
                        new_line[1] = str(int(new_line[1]) + 1)
                    else:
                        new_line[2] = str(int(new_line[2]) + 1)
                    new_line = ",".join(new_line)
                    new_line += "\n"
                    lunch_data[idx] = new_line

            if not modified:
                new_line = f"{date},0,0\n"
                lunch_data.append(new_line)
            fp.truncate(0)
            fp.writelines(lunch_data)
    except Exception as err:
        print(err)
        with open(filename, "w") as fd:
            lunch_data = ["DATUM,NTI,PROCIVITAS\n"]
            if school == "NTI":
                lunch_data.append(f"{date},1,0")
            else:
                lunch_data.append(f"{date},0,1")
            fd.writelines(lunch_data)

def handle_input(mfr, tags, times, now, used_tags, data_filename):
    """ 
    Based on the response of the scanned tag, different results will be returned.

    When a tag is scanned, different results will appear, based on what the conditions of the tag is.
    If the tag's id does not match one of the tag-ids in id.csv, the function will return False and the message "OKÄND NYCKELTAGG".
    If the tag does not have a matching "lunch_time", the function will return False and the message "INGEN MATCHANDE LUNCHTID". This will happen when the id is in the system,
    but does not have a class.
    If the tag does have a matching "lunch_time" but the tag is scanned outside of its matching time, the function will return False and the message "DIN LUNCHTID ÄR {lunch_start}-{lunch_end}".
    together with the time that the tag scan would result in a "GODKÄND SKANNING! SMAKLIG MÅLTID!" message.
    If the tag has already been scanned , the screen will display the message "DU HAR REDAN SKANNAT".
    """

    tag_match = find_matching_tag(mfr, tags)
    if(not (len(tag_match) > 0)):
        return False, "OKÄND NYCKELTAGG"

    times_match = find_matching_lunch_time(tag_match[0], times)

    # If the tag is in the system but not registered to a class
    if(not (len(times_match) > 0)):
        return False, "INGEN MATCHANDE LUNCHTID"

    # Hashes the scanned tag
    hashed = hashlib.sha256(str(tag_match[1]).encode('ASCII')).hexdigest()

    if(not (valid_lunch_time(times_match, now))):
        lunch_start, lunch_end = lunch_time(times_match, now)
        return False, f"DIN LUNCHTID ÄR {lunch_start}-{lunch_end}"

    if hashed in used_tags:
        return False, "DU HAR REDAN SKANNAT"

    # Adds the recently hashed tag into a list
    used_tags.append(hashed)
    save_students_eaten(now, tag_match[2], data_filename)
    return True, "GODKÄND SKANNING! SMAKLIG MÅLTID!"

def lunch_time(times_match, now):
    """ 
    The function calculates the current weekday and returns lunch_start and lunch_end from the list in "tider" csv file for the respective weekday.
    
    If there is no valid lunch_start or lunch_end time, for example if a tag is scanned during a weekend, the function will return "00:00","00:00".
    """
    try:
        weekday = now.weekday()
        lunch_start = times_match[weekday + 1].split("-")[0]
        lunch_end = times_match[weekday + 1].split("-")[1]
        return lunch_start, lunch_end
    except:
        return "00:00","00:00"

def valid_lunch_time(times_match, now):
    """ 
    Uses the total minutes and total hours and compares them to the total minutes of "lunch_start" and "lunch_end" to determine if it is a valid lunch time or not.
    """
    lunch_start, lunch_end = lunch_time(times_match, now)
    lunch_start_in_min = get_time_in_min(lunch_start)
    lunch_end_in_min = get_time_in_min(lunch_end)
    now_in_min = get_time_in_min(f"{now.hour}:{now.minute}")
    return lunch_start_in_min <= now_in_min <= lunch_end_in_min

def key_press(key):
    """ 
    Creates a global variable for keypresses and appends them to "key_press".
    """
    global key_presses
    key_presses.append(key)

def handle_esc(window):
    """ 
    If escape if pressed, the window will be shut down after 1 second.
    """
    global timer
    if timer:
        timer.cancel()
    window.bye()
    time.sleep(1)
    sys.exit(0)


def play_sound():
    """ 
    Allows sound to be played.
    """
    global denied_sound
    os.system('mpg123 ' + denied_sound)
# Sound can only play on Linux
# This function only plays sound when on Linux
def start_sound():
    """ 
    If the operating system is linux the variable "sound_t" will be used to play the sound.

    If the operating systemis not linux, no sound will be played.
    """
    if platform.system() == "Linux":
        global sound_t
        sound_t = multiprocessing.Process(target=play_sound)
        sound_t.start()

# If os is Linux, sets the display to fullscreen
def os_checker():
    """ 
    Makes the ui into fullscreen if the operating system is Linux.
    """
    if platform.system() == "Linux":
        root.attributes("-fullscreen", True)

    """ 
    <><><><><><><><><><><><><> JaG bEhÖvEr HjÄlP mEd AtT kOmMeNtErA dEn HäR dElEn Av KoDeN <><><><><><><><><><><><><>
    """
if __name__ == '__main__':
    # Path to the working directory
    file = os.path.dirname(os.path.realpath(__file__))

    if "-test" in sys.argv:
        tags_root = get_file_data(file+"/id_tester.csv", "tags")
        times_root = get_file_data(file+"/tider_tester.csv", "times")
    else:
        tags_root = get_file_data(file+"/id.csv", "tags")
        times_root = get_file_data(file+"/tider.csv", "times")

    data_file = "lunch_data.csv"

    if "--data" in sys.argv:
        try:
            data_file = sys.argv[sys.argv.index("--data") + 1]
        except:
            print("YOU NEED TO SPECIFY A DATA FILE WITH --data flag")

    skanna_tagg = "VÄNLIGEN SKANNA DIN TAGG TILL VÄNSTER"

    window = turtle.Screen()
    window.setup(width = 1.0, height = 1.0)
    turtle.hideturtle()
    window.title("Lunchpad")

    # Remove close, minimize, maximize buttons:
    canvas = window.getcanvas()
    root = canvas.winfo_toplevel()
    root.overrideredirect(1)
    os_checker()

    window.bgcolor("black")
    turtle.color('white')
    style = ('Roboto', 50, 'bold')
    turtle.write(skanna_tagg, font=style, align='center')

    timer = None

    denied_sound = "/home/pi/Desktop/lunchpad/denied.mp3"
    sound_t = None
    key_presses = []
    used_tags = []

    window.onkey(lambda: key_press("0"), "0")
    window.onkey(lambda: key_press("1"), "1")
    window.onkey(lambda: key_press("2"), "2")
    window.onkey(lambda: key_press("3"), "3")
    window.onkey(lambda: key_press("4"), "4")
    window.onkey(lambda: key_press("5"), "5")
    window.onkey(lambda: key_press("6"), "6")
    window.onkey(lambda: key_press("7"), "7")
    window.onkey(lambda: key_press("8"), "8")
    window.onkey(lambda: key_press("9"), "9")
    window.onkey(lambda: handle_enter(window, style), "Return")
    window.onkey(lambda: handle_esc(window), "Escape")
    window.listen()
    window.mainloop()
