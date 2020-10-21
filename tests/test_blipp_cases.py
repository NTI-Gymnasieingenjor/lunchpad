#!/usr/bin/env python3
import subprocess, time, os, signal, psutil
from pynput.keyboard import Key, Controller

args = ["./lunchpad.py"]
p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

tests = [
    ["12348910", "Okänd nyckeltagg"],
    ["***REMOVED***", "Nekat"],
    ["***REMOVED***", "Godkänt"]
]

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
    res = p.stdout.readline().decode("utf-8").strip()
    if res == test[1]:
        print("\u001b[32mTest successful\u001b[0m")
    else:
        print("\u001b[31mTest failed\u001b[0m")

