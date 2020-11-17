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

# Reads respective csv file and adds the content into a list
def get_file_data(filepath, mode="tags"):
    data = []
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            line_data = line.rstrip().split(",")
            if(mode == "tags"):
                data.append(line_data)
            elif(mode == "times"):
                data.append(line_data)
            else:
                print("Invalid mode.")
            line = fp.readline()
            cnt += 1
    return data


# Looks through all the tags and returns the tag and the corresponding class,
# otherwise it returns an empty list
def find_matching_tag(tag, tags):
    match = list(filter(lambda x: tag in x, tags))
    if(len(match) > 0):
        return match[0]
    else:
        return match

# Uses the matched class to find and return the corresponding lunch time
def find_matching_lunch_time(grade, times):
    match = list(filter(lambda x: grade in x, times))
    if(len(match) > 0):
        return match[0]
    else:
        return match

# Takes a time value, for example 12:00 and splits it,
# then converts it into minutes
def get_time_in_min(timestamp):
    hours, minutes = timestamp.split(":")
    total_minutes = int(hours)*60+int(minutes)
    return total_minutes


def write_text_turtle(window, turtle, style, granted, msg=""):
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
        global timer
        turtle.clear()
        turtle.write(skanna_tagg, font=style, align='center')
        turtle.bgcolor("black")
        timer = None

    timer = threading.Timer(3.0, _timeout)
    timer.start()


def handle_enter(window, style):

    global timer, sound_t, file
    if timer:
        timer.cancel()
    if sound_t and sound_t.is_alive():
        sound_t.terminate()

    window.bgcolor("black")
    turtle.color('white')
    turtle.clear()

    # "mfr" variable refers to the MFR ID,
    # Displayed on the back of the tag
    global key_presses
    mfr = "".join(key_presses)
    key_presses = []
    allowed, message = handle_input(mfr, tags_root, times_root, datetime.datetime.now(), used_tags)
    write_text_turtle(window, turtle, style, allowed, message)
    print(message)
    if allowed == False:
        start_sound()

def save_students_eaten():
    """ Saves the students eaten data to lunch_data.csv """
    global nti_eaten
    global procivitas_eaten
    global date

    with open("lunch_data.csv", "r+") as fp:
        lunch_data = fp.readlines()
        modified = False
        for idx, line in enumerate(lunch_data):
            line = line.replace('\x00', '')
            lunch_data[idx] = line
            if date in line:
                modified = True
                new_line = line.split(",")
                new_line[1] = str(nti_eaten)
                new_line[2] = str(procivitas_eaten)
                new_line = ",".join(new_line)
                new_line += "\n"
                lunch_data[idx] = new_line

        if not modified:
            new_line = f"{date},{nti_eaten},{procivitas_eaten}\n"
            lunch_data.append(new_line)
        fp.truncate(0)
        fp.writelines(lunch_data)

def validate_date_variable():
    """ Checks if the date variable is equal to today. If not it resets nti_eaten, procivitas_eaten and sets date to todays date """
    global nti_eaten
    global procivitas_eaten
    global date

    if date != datetime.datetime.today().strftime('%Y-%m-%d'):
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        nti_eaten = 0
        procivitas_eaten = 0

def handle_input(mfr, tags, times, now, used_tags):
    global nti_classes
    global procivitas_classes
    global nti_eaten
    global procivitas_eaten

    tag_match = find_matching_tag(mfr, tags)
    if(not (len(tag_match) > 0)):
        return False, "OKÄND NYCKELTAGG"

    times_match = find_matching_lunch_time(tag_match[0], times)

    # If the tag is in the system but not registered to a class
    if(not (len(times_match) > 0)):
        return False, "INGEN MATCHANDE LUNCHTID"

    hashed = hashlib.sha256(str(tag_match[1]).encode('ASCII')).hexdigest()

    if(valid_lunch_time(times_match, now)):
        if hashed in used_tags:
            return False, "DU HAR REDAN SKANNAT"


        used_tags.append(hashed)
        validate_date_variable()
        if tag_match[0] in nti_classes:
            nti_eaten += 1
        else:
            procivitas_eaten += 1
        save_students_eaten()
        return True, "GODKÄND SKANNING! SMAKLIG MÅLTID!"


    else:
        lunch_start, lunch_end = lunch_time(times_match, now)
        return False, f"DIN LUNCHTID ÄR {lunch_start}-{lunch_end}"

def lunch_time(times_match, now):
    weekday = now.weekday()
    lunch_start = times_match[weekday + 1].split("-")[0]
    lunch_end = times_match[weekday + 1].split("-")[1]
    return lunch_start, lunch_end

def valid_lunch_time(times_match, now):
    lunch_start, lunch_end = lunch_time(times_match, now)
    lunch_start_in_min = get_time_in_min(lunch_start)
    lunch_end_in_min = get_time_in_min(lunch_end)
    now_in_min = get_time_in_min(f"{now.hour}:{now.minute}")
    return lunch_start_in_min <= now_in_min <= lunch_end_in_min

def key_press(key):
    global key_presses
    key_presses.append(key)

def handle_esc(window):
    global timer
    if timer:
        timer.cancel()
    window.bye()
    time.sleep(1)
    sys.exit(0)


def play_sound():
    global denied_sound
    os.system('mpg123 ' + denied_sound)
# Sound can only play on Linux
# This function only plays sound when on Linux
def start_sound():
    if platform.system() == "Linux":
        global sound_t
        sound_t = multiprocessing.Process(target=play_sound)
        sound_t.start()

# If os is Linux, sets the display to fullscreen
def os_checker():
    if platform.system() == "Linux":
        root.attributes("-fullscreen", True)

def load_lunch_data():
    global nti_eaten
    global procivitas_eaten

    """ Loads students eaten data from lunch_data.csv """
    try:
        with open("lunch_data.csv", "r") as f:
            for line in f:
                if date in line:
                    nti_eaten = int(line.split(",")[1].rstrip())
                    procivitas_eaten = int(line.split(",")[2].rstrip())
    except Exception as err:
        with open("lunch_data.csv", "w") as f:
            f.writelines(["DATUM,NTI,PROCIVITAS\n"])
        print(err)

if __name__ == '__main__':
# Path to the working directory
    file = os.path.dirname(os.path.realpath(__file__))

    nti_classes = ["1A_SA", "1B_ES", "1C_NA", "1D_TE", "1E_EE", "1F_TE", "1G_TE", "2A_SA", "2B_ES", "2C_NA", "2C_TE", "2D_TE", "2E_EE", "2F_TE", "3A_SA", "3B_ES", "3C_NA", "3D_TE", "3E_EE", "3F_TE", "TE4", "Cool"]
    procivitas_classes = ["Ek20", "Na20", "Sa20"]

    date = datetime.datetime.today().strftime('%Y-%m-%d')

    nti_eaten = 0
    procivitas_eaten = 0

    # Loads data from lunch_data.csv
    load_lunch_data()

    tags_root = get_file_data(file+"/id.csv", "tags")
    times_root = get_file_data(file+"/tider.csv", "times")

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
