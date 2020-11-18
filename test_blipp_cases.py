#!/usr/bin/env python3
import subprocess, time, psutil, sys
from pynput.keyboard import Key, Controller
from lunchpad import *
import datetime

def correct_output():
    global tests
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

def correct_text():

    actual = handle_input("***REMOVED***", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10),[])
    expected = True, "GODKÄND SKANNING! SMAKLIG MÅLTID!"
    check_test(expected, actual)

    actual = handle_input("***REMOVED***", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10),[])
    expected = False, "DIN LUNCHTID ÄR 11:00-11:20"
    check_test(expected, actual)
    
    actual = handle_input("***REMOVED***", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10),[])
    expected = False, "INGEN MATCHANDE LUNCHTID"
    check_test(expected, actual)

    actual = handle_input("123456789", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10),[])
    expected = False, "OKÄND NYCKELTAGG"
    check_test(expected, actual)

    actual = handle_input("***REMOVED***", tags, times, datetime.datetime(2020, 11, 14, 12, 10, 10),[])
    expected = False, "DIN LUNCHTID ÄR 00:00-00:00"
    check_test(expected, actual)


def time_test():

    # On time for lunch
    correct_time = valid_lunch_time(["TE4","12:10-12:30","12:10-12:30","12:10-12:30","12:30-12:50","12:30-12:50"], datetime.datetime(2020, 11, 11, 12, 10, 10))
    # 1 minute before lunch time
    wrong_before_1min = valid_lunch_time(["TE4","12:10-12:30","12:10-12:30","12:10-12:30","12:30-12:50","12:30-12:50"], datetime.datetime(2020, 11, 11, 12, 9, 10))
    # 1 minute after lunch time
    wrong_after_1min = valid_lunch_time(["TE4","12:10-12:30","12:10-12:30","12:10-12:30","12:30-12:50","12:30-12:50"], datetime.datetime(2020, 11, 11, 12, 9, 10))
    # Midnight
    wrong_time_midnight = valid_lunch_time(["TE4","12:10-12:30","12:10-12:30","12:10-12:30","12:30-12:50","12:30-12:50"], datetime.datetime(2020, 11, 11, 0, 0, 1))
    # Weekend
    wrong_time_weekend = valid_lunch_time(["TE4","12:10-12:30","12:10-12:30","12:10-12:30","12:30-12:50","12:30-12:50"], datetime.datetime(2020, 11, 14, 16, 0, 1))

    check_test(True, correct_time)
    check_test(False, wrong_before_1min)
    check_test(False, wrong_after_1min)
    check_test(False, wrong_time_midnight)
    check_test(False, wrong_time_weekend)
    
def check_test(expected, actual):
    if expected == actual:
        print("\u001b[32mTest successful\u001b[0m")
    else:
        print("\u001b[31mTest failed\u001b[0m")
        print("Expected:", expected)
        print("Actual:", actual)
        fail + 1
        return fail


def fail_check(fail):
    if fail >= 1:
        sys.exit(1)

if __name__ == '__main__':
    args = ["python3","lunchpad.py","-test"]

    file = os.path.dirname(os.path.realpath(__file__))

    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    tags = get_file_data(file+"/id_tester.csv", "tags")
    times = get_file_data(file+"/tider_tester.csv", "times")


    tests = [
        ["12348910", "OKÄND NYCKELTAGG"],
        ["***REMOVED***", "GODKÄND SKANNING! SMAKLIG MÅLTID!"],
        ["***REMOVED***", "DU HAR REDAN SKANNAT"]
    ]

    fail = 0

    print("Correct_output")
    correct_output()
    print("Time_test")
    time_test()
    print("Correct_text")
    correct_text()
    fail_check(fail)
