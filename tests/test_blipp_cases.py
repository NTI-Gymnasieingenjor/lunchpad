#!/usr/bin/env python3
import subprocess
import time
from pynput.keyboard import Key, Controller

args = ["./lunchpad.py"]
p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

time.sleep(2)
keyboard = Controller()

keyboard.type("1234")
keyboard.press(Key.enter)
keyboard.release(Key.enter)

time.sleep(1)

keyboard.type("536956614")
keyboard.press(Key.enter)
keyboard.release(Key.enter)

out, err = p.communicate()
res = str(out).split("\n")
print(res)
