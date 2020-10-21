#!/usr/bin/env python3
import subprocess, time, os, signal
from pynput.keyboard import Key, Controller

args = ["./lunchpad.py"]
p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

time.sleep(2)
keyboard = Controller()

# Tests with invalid MFR
keyboard.type("12348910")
keyboard.press(Key.enter)
keyboard.release(Key.enter)

time.sleep(1)

# Tests with valid MFR but invalid time
keyboard.type("536956614")
keyboard.press(Key.enter)
keyboard.release(Key.enter)

time.sleep(1)

# Tests with valid MFR at correct time
keyboard.type("100331417")
keyboard.press(Key.enter)
keyboard.release(Key.enter)

#out, err = p.communicate()

print(p.stdout)

#res = out.decode("utf-8").split("\n")
#res.pop(-1)

os.kill(p.pid, 9)
