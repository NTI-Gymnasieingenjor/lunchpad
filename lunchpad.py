#!/usr/bin/env python3
import datetime
import time
import turtle
import threading
import math
import sys, os

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

file = os.path.dirname(os.path.realpath(__file__))

tags = get_file_data(file+"/id.csv", "tags")
times = get_file_data(file+"/tider.csv", "times")

def find_matching_tag(tag="536956614"):
    match = list(filter(lambda x: tag in x, tags))
    if(len(match) > 0):
        return match[0]
    else:
        return match

def find_matching_lunch_time(grade=""):
    match = list(filter(lambda x: grade in x, times))
    if(len(match) > 0):
        return match[0]
    else:
        return match

def get_time_in_minutes(timestamp):
    hours, minutes = timestamp.split(":")
    return int(hours)*60+int(minutes)

def write_text_turtle(window, turtle, style, granted, msg=""):
    global active
    turtle.write(msg, font=style, align='center')
    if(granted):
        window.bgcolor("#5cb85c")
    else:
        window.bgcolor("#ED4337")
    blipp_your_tagg()


timer = None
def blipp_your_tagg():
    global timer
    global style
    def _timeout():
        global timer
        turtle.clear()
        turtle.write("VÄNLIGEN SKANNA DIN NYCKELTAGG NEDAN", font=style, align='center')
        turtle.bgcolor("black")
        timer = None

    timer = threading.Timer(3.0, _timeout)
    timer.start()

key_presses = []
def handle_enter(window, style):
    global timer
    if timer:
        timer.cancel()
    window.bgcolor("black")
    turtle.color('white')
    turtle.clear()
    global key_presses
    mfr = "".join(key_presses)
    key_presses = []
    tag_match = find_matching_tag(mfr)
    if(len(tag_match) > 0):
        times_match = find_matching_lunch_time(tag_match[0])
        if(len(times_match) > 0):
            weekday = datetime.datetime.today().weekday()
            now = datetime.datetime.now()

            lunch_start = times_match[weekday + 1].split("-")[0]
            lunch_end = times_match[weekday + 1].split("-")[1]
            lunch_start_in_m = get_time_in_minutes(lunch_start)
            lunch_end_in_m = get_time_in_minutes(lunch_end)
            now_in_m = get_time_in_minutes(f"{now.hour}:{now.minute}")

            if((now_in_m >= lunch_start_in_m) and (now_in_m <= lunch_end_in_m)):
                print("Godkänt")
                write_text_turtle(window, turtle, style, True, "GODKÄND SKANNING! SMAKLIG MÅLTID!")
            else:
                print("Nekat")
                write_text_turtle(window, turtle, style, False, f"DIN LUNCHTID ÄR MELLAN {lunch_start}-{lunch_end}")
        else:
            print("Ingen matchande lunchtid")
            write_text_turtle(window, turtle, style, False, "ERROR: INGEN MATCHANDE LUNCHTID")
    else:
        write_text_turtle(window, turtle, style, False, "OKÄND NYCKELTAGG")
        print("Okänd nyckeltagg")

def key_press(key):
    global key_presses
    key_presses.append(key)

window = turtle.Screen()
window.setup(width = 1.0, height = 1.0)
turtle.hideturtle()
window.title("Lunchpad")

#remove close,minimaze,maximaze buttons:
canvas = window.getcanvas()
root = canvas.winfo_toplevel()
root.overrideredirect(1)
root.attributes("-fullscreen", True)

window.bgcolor("black")
turtle.color('white')
style = ('Roboto', 30, 'bold')
turtle.write("VÄNLIGEN SKANNA DIN NYCKELTAGG NEDAN", font=style, align='center')
# Register keys

def handle_esc(window):
    global timer
    if timer:
        timer.cancel()
    window.bye()
    time.sleep(1)
    sys.exit(0)

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
