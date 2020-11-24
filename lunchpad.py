#!/usr/bin/env python3
import datetime
import time
import turtle
import threading
import sys
import os
import multiprocessing
import hashlib
import platform


# Reads respective csv file and adds the content into a list
def get_file_data(filepath, mode="tags"):
    data = []
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            line_data = line.rstrip().split(",")
            data.append(line_data)
            line = fp.readline()
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
    allowed, message = handle_input(mfr, tags_root, times_root, datetime.datetime.now(), used_tags, data_file)
    write_text_turtle(window, turtle, style, allowed, message)
    print(message)
    if allowed is False:
        start_sound()


def save_students_eaten(date, school, filename):
    """ Saves the students eaten data to lunch_data.csv """

    date = date.strftime('%Y-%m-%d')

    try:
        new_lunch_data = None
        with open(filename, "r+") as fp:
            lunch_data = fp.readlines()
            modified = False
            # Goes through all rows in lunch data.
            for idx, line in enumerate(lunch_data):
                if date in line:
                    modified = True
                    line = line.replace("\n", "")
                    new_line = line.split(",")
                    # Increases the value of how many people have successfully scanned for the day.
                    if school == "NTI":
                        new_line[1] = str(int(new_line[1]) + 1)
                    else:
                        new_line[2] = str(int(new_line[2]) + 1)
                    new_line = ",".join(new_line)
                    new_line += "\n"
                    lunch_data[idx] = new_line
                    break
            
            # If no row with todays date is found, create a new row.
            if not modified:
                new_line = f"{date},0,0\n"
                lunch_data.append(new_line)

            new_lunch_data = lunch_data

        with open(filename, "w") as fd:
            fd.writelines(new_lunch_data)

    except Exception as err:
        print(err)
        # Create lunch_data.csv file if it doesn't exist.
        with open(filename, "w") as fd:
            lunch_data = ["DATUM,NTI,PROCIVITAS\n"]
            if school == "NTI":
                lunch_data.append(f"{date},1,0")
            else:
                lunch_data.append(f"{date},0,1")
            fd.writelines(lunch_data)


def handle_input(mfr, tags, times, now, used_tags, data_filename):

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
    try:
        weekday = now.weekday()
        lunch_start = times_match[weekday + 1].split("-")[0]
        lunch_end = times_match[weekday + 1].split("-")[1]
        return lunch_start, lunch_end
    except Exception:
        return "00:00", "00:00"


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
        except Exception:
            print("YOU NEED TO SPECIFY A DATA FILE WITH --data flag")

    skanna_tagg = "VÄNLIGEN SKANNA DIN TAGG TILL VÄNSTER"

    window = turtle.Screen()
    window.setup(width=1.0, height=1.0)
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
