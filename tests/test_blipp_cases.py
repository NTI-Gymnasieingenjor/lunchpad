#!/usr/bin/env python3
import subprocess, time, os, signal, psutil, sys
from pynput.keyboard import Key, Controller

args = ["python","lunchpad.py"]
p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

tests = [
    ["12348910", "Okänd nyckeltagg"],
    ["536956614", "Nekat"],
    ["101129785", "Godkänt"],
    ["101129785", "Dubbel skann"]
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
    res = p.stdout.readline().decode("latin-1").strip()
    if res == test[1]:
        print("\u001b[32mTest successful\u001b[0m")
    else:
        print("\u001b[31mTest failed\u001b[0m")
        sys.exit(1)

