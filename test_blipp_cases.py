#!/usr/bin/env python3
import subprocess, time, psutil, sys
from pynput.keyboard import Key, Controller
from lunchpad import *
import datetime

def correct_text():
    time.sleep(2)
    keyboard = Controller()

    for test in tests:
        keyboard.type(test[0])
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(1)
        
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)

    for test in tests:
        res = p.stdout.readline().decode("latin-1").strip()
        check_test(test[1], res)

def check_test(expected, actual):
    if expected == actual:
        print("\u001b[32mTest successful\u001b[0m")
    else:
        print("\u001b[31mTest failed\u001b[0m")
        sys.exit(1)

def time_test():
    check_test(True, correct_time)
    check_test(False, wrong_before_1min)
    check_test(False, wrong_after_1min)
    check_test(False, wrong_time_midnight)


if __name__ == '__main__':
    args = ["python","lunchpad.py"]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    tests = [
        ["12348910", "Okänd nyckeltagg"],
        ["536956614", "Nekat"],
        ["101129785", "Godkänt"],
        ["101129785", "Dubbel skann"]
    ]
    # On time for lunch
    correct_time = valid_lunch_time(["TE4","12:10-12:30","12:10-12:30","12:10-12:30","12:30-12:50","12:30-12:50"], datetime.datetime(2020, 11, 11, 12, 10, 10))
    # 1 minute before lunch time
    wrong_before_1min = valid_lunch_time(["TE4","12:10-12:30","12:10-12:30","12:10-12:30","12:30-12:50","12:30-12:50"], datetime.datetime(2020, 11, 11, 12, 9, 10))
    # 1 minute after lunch time
    wrong_after_1min = valid_lunch_time(["TE4","12:10-12:30","12:10-12:30","12:10-12:30","12:30-12:50","12:30-12:50"], datetime.datetime(2020, 11, 11, 12, 9, 10))
    # Midnight
    wrong_time_midnight = valid_lunch_time(["TE4","12:10-12:30","12:10-12:30","12:10-12:30","12:30-12:50","12:30-12:50"], datetime.datetime(2020, 11, 11, 0, 0, 1))

    print("Correct_text")
    correct_text()
    print("Time_test")
    time_test()