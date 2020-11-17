#!/usr/bin/env python3
import subprocess, os, time
from pynput.keyboard import Key, Controller

valid_tags = ["100331417", "101129785"]
nti_tag = "100331417"
filename = "lunch_data.csv"

keyboard = Controller()

# TEST FÖR GRÖNTAGG
print("[*] Testing with 1 green tag")
try:
    os.remove(filename)
except:
    pass
lunchpad = subprocess.Popen(["python3", "lunchpad.py"])

time.sleep(1)
# Skriva in tagg.
keyboard.type(nti_tag)
keyboard.press(Key.enter)
keyboard.release(Key.enter)

time.sleep(1)

# Kolla efter csv filen
try:
    with open(filename, "r") as f:
        # Kolla så csv filen har värdet 1 i rätt kolumn
        f.readline() # Reads first line and does nothing with it.
        line = f.readline()
        date, nti, procivitas = line.split(",")
        if nti.rstrip() == "1" and procivitas.rstrip() == "0":
            print("TEST COMPLETE")
        else:
            print("TEST FAILED")
except Exception as err:
    print("TEST FAILED")
    print(err)

keyboard.press(Key.esc)
keyboard.release(Key.esc)
lunchpad.terminate()

# TEST FÖR TVÅ GRÖNTAGGAR
print("[*] Testing with 2 green tags")
try:
    os.remove(filename)
except:
    pass
lunchpad = subprocess.Popen(["python3", "lunchpad.py"])

time.sleep(1)

keyboard.type(valid_tags[0])
keyboard.press(Key.enter)
keyboard.release(Key.enter)

time.sleep(1)

keyboard.type(valid_tags[1])
keyboard.press(Key.enter)
keyboard.release(Key.enter)

time.sleep(1)

# Kolla efter csv filen
try:
    with open(filename, "r") as f:
        f.readline() # Reads first line and does nothing with it.
        line = f.readline()
        date, nti, procivitas = line.split(",")
        if nti.rstrip() == "2" and procivitas.rstrip() == "0":
            print("TEST COMPLETE")
        else:
            print("TEST FAILED")
except Exception as err:
    print("TEST FAILED")
    print(err)

keyboard.press(Key.esc)
keyboard.release(Key.esc)
lunchpad.terminate()
