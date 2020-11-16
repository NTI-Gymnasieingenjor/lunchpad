#!/usr/bin/env python3
import datetime
import time
import turtle
import threading
import sys, os
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
    # displayed on the back of the tag
    global key_presses
    mfr = "".join(key_presses)
    key_presses = []
    allowed, message = handle_input(mfr, tags_root, times_root, datetime.datetime.now(), used_tags)
    write_text_turtle(window, turtle, style, allowed, message)
    print(message)
    if allowed == False:
        start_sound()


def handle_input(mfr, tags, times, now, used_tags):

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
    

if __name__ == '__main__':
# Path to the working directory
    file = os.path.dirname(os.path.realpath(__file__))

    tags_root = get_file_data(file+"/id.csv", "tags")
    times_root = get_file_data(file+"/tider.csv", "times")

    skanna_tagg = "VÄNLIGEN SKANNA DIN TAGG TILL VÄNSTER"

    window = turtle.Screen()
    window.setup(width = 1.0, height = 1.0)
    turtle.hideturtle()
    window.title("Lunchpad")

    # remove close,minimaze,maximaze buttons:
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