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
    Looks through all the tags and returns the tag and its corresponding class, otherwise it returns an empty list.
    """
    match = list(filter(lambda x: tag in x, tags))
    if(len(match) > 0):
        return match[0]
    else:
        return match

def find_matching_lunch_time(grade, times):
    """
    Uses the class of the corresponding tag to find the matching lunch times, then returns the matched lunch times.
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
    """
    hours, minutes = timestamp.split(":")
    total_minutes = int(hours)*60+int(minutes)
    return total_minutes


def write_text_turtle(window, turtle, style, granted, msg=""):
    """
    Makes the display background green or red based on if granted is true or not.
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
        Default display for the ui. Returns to it 3 seconds after a scan.
        """
        global timer
        turtle.clear()
        turtle.write(skanna_tagg, font=style, align='center')
        turtle.bgcolor("black")
        timer = None

    timer = threading.Timer(3.0, _timeout)
    timer.start()


def handle_enter(window, style):
    """-
    This function runs everytime a tag is scanned. It plays sound, stores keypresses and writes the background color and respective message.
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
    """
    Saves the students eaten data to lunch_data.csv
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
    Based on different conditions, when a tag is scanned, the function will return a True or False and its respective message.
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
    Function will return lunch_start and lunch_end based on the current weekday and relative to times_match, or if a tag is scanned on the weekend it will return "00:00","00:00".
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
    Checks if it is a valid lunch time when a tag is scanned, based on lunch_start, lunch_end and current time converted into minutes using the get_time_in_min function.
    """
    lunch_start, lunch_end = lunch_time(times_match, now)
    lunch_start_in_min = get_time_in_min(lunch_start)
    lunch_end_in_min = get_time_in_min(lunch_end)
    now_in_min = get_time_in_min(f"{now.hour}:{now.minute}")
    return lunch_start_in_min <= now_in_min <= lunch_end_in_min

def key_press(key):
    """
    Appends keypresses into key_presses list.
    """
    global key_presses
    key_presses.append(key)

def handle_esc(window):
    """
    If escape if pressed, the window will be terminated after 1 second.
    """
    global timer
    if timer:
        timer.cancel()
    window.bye()
    time.sleep(1)
    sys.exit(0)


def play_sound():
    """
    Function to add sound player and sound.
    """
    global denied_sound
    os.system('mpg123 ' + denied_sound)
# Sound can only play on Linux
# This function only plays sound when on Linux
def start_sound():
    """
    Function used to play the sound from play_sound function. Will only play if the operating system is Linux, since it crashes when used on Windows.
    """
    if platform.system() == "Linux":
        global sound_t
        sound_t = multiprocessing.Process(target=play_sound)
        sound_t.start()

# If os is Linux, sets the display to fullscreen
def os_checker():
    """ 
    Sets the ui into fullscreen if the operating system is Linux. Will crash on Windows.
    """
    if platform.system() == "Linux":
        root.attributes("-fullscreen", True)

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
