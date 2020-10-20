import datetime
import time
import turtle
from playsound import playsound

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

tags = get_file_data("./id.csv", "tags")
times = get_file_data("./tider.csv", "times")

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


while True:
    mfr = input()
    tag_match = find_matching_tag(mfr)
    window = turtle.Screen()
    window.bgcolor("black")
    turtle.color('white')
    style = ('Roboto', 30, 'bold')
    turtle.clear()
    if(len(tag_match) > 0):
        times_match = find_matching_lunch_time(tag_match[0])
        if(len(times_match) > 0):
            weekday = datetime.datetime.today().weekday()
            now = datetime.datetime.now()
            lunch_in_m = get_time_in_minutes(times_match[weekday + 1])
            now_in_m = get_time_in_minutes(f"{now.hour}:{now.minute}")
            if((now_in_m >= lunch_in_m) and (now_in_m <= lunch_in_m + 20)):
                print("Du får äta")
                turtle.write('DU FÅR ÄTA', font=style, align='center')
                turtle.hideturtle()
                window.bgcolor("#5cb85c")
            else:
                print("Du får inte äta")
                turtle.write('DU FÅR INTE ÄTA', font=style, align='center')
                turtle.hideturtle()
                window.bgcolor("#ED4337")
                playsound('denied.mp3')
        else:
            print("Couldnt find any matching time with your tag")
            turtle.write('INGEN MATCHANDE LUNCH TID', font=style, align='center')
            turtle.hideturtle()
            window.bgcolor("#ED4337")
            playsound('denied.mp3')
    else:
        print("Couldnt find any match with your tag")
        turtle.write('OKÄND TAG', font=style, align='center')
        turtle.hideturtle()
        window.bgcolor("#ED4337")
        playsound('denied.mp3')

