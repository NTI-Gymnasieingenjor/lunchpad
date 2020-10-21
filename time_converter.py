#!/usr/bin/env python3
import datetime
import time
import turtle
import threading
import math
import sys

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

times = get_file_data("./tider.csv", "times")


for data in times:
    def gen(arr):
        arr = arr.split(":")
        new_hour = int(arr[0])
        new_min = int(arr[1])+20
        if new_min >= 60:
            new_min -= 60
            new_hour += 1
        return "{:>02}:{:>02}".format(new_hour, new_min)
    data[1] = "{}-{}".format(data[1], gen(data[1]))
    data[2] = "{}-{}".format(data[2], gen(data[2]))
    data[3] = "{}-{}".format(data[3], gen(data[3]))
    data[4] = "{}-{}".format(data[4], gen(data[4]))
    data[5] = "{}-{}".format(data[5], gen(data[5]))

print(times)
with open("tider_test.csv", "w") as f:
    for data in times:
        f.write(",".join(data))
        f.write("\n")
