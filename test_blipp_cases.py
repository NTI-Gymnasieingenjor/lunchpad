#!/usr/bin/env python3
import subprocess
import time
from pynput.keyboard import Key, Controller
from lunchpad import *
import datetime
import platform
import unittest


class TestLunchpad(unittest.TestCase):

    def test_correct_output(self):
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

        # Uses latin-8 charset instead of utf-8 on Windows machines to avoid an error.
        for test in tests:
            charset = "latin-1"
            if platform.system() == "Linux":
                charset = "utf-8"
            res = p.stdout.readline().decode(charset).strip()
            self.assertEqual(test[1], res)

    def test_correct_text(self):
        # Scanned tag is on time, NTI tag
        actual = handle_input("900865598", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10), [], "test_data.csv")
        expected = True, "GODKÄND SKANNING! SMAKLIG MÅLTID!"
        self.assertEqual(expected, actual)

        # Scanned tag is on time, Procivitas tag
        actual = handle_input("739341266", tags, times, datetime.datetime(2020, 11, 11, 12, 20, 10), [], "test_data.csv")
        expected = True, "GODKÄND SKANNING! SMAKLIG MÅLTID!"
        self.assertEqual(expected, actual)

        # Scanned tag is first in list
        actual = handle_input("900865598", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10), ["78b70d2dec5594fe350af13afd2ec839695442053013ec3e2d7386429b5764b4", "2711ec7bebeff204b1d6d39cc8dcbfbef44d93da919befb9834a839d98a5e1bf"], "test_data.csv")
        expected = False, "DU HAR REDAN SKANNAT"
        self.assertEqual(expected, actual)

        # Scanned tag is last in list
        actual = handle_input("900865598", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10), ["2711ec7bebeff204b1d6d39cc8dcbfbef44d93da919befb9834a839d98a5e1bf", "78b70d2dec5594fe350af13afd2ec839695442053013ec3e2d7386429b5764b4"], "test_data.csv")
        expected = False, "DU HAR REDAN SKANNAT"
        self.assertEqual(expected, actual)

        # Scanned tag is in the middle of the list
        actual = handle_input("900865598", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10), ["2711ec7bebeff204b1d6d39cc8dcbfbef44d93da919befb9834a839d98a5e1bf", "78b70d2dec5594fe350af13afd2ec839695442053013ec3e2d7386429b5764b4", "1514aa8277131f9dc6c69f615fae6e15cce2022237a5c98a3533f2007bb99aba"], "test_data.csv")
        expected = False, "DU HAR REDAN SKANNAT"
        self.assertEqual(expected, actual)

        # Scanned tag is off time, NTI tag
        actual = handle_input("754729301", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10), [], "test_data.csv")
        expected = False, "DIN LUNCHTID ÄR 11:00-11:20"
        self.assertEqual(expected, actual)

        # Scanned tag is off time, Procivitas tag
        actual = handle_input("739341266", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10), [], "test_data.csv")
        expected = False, "DIN LUNCHTID ÄR 12:20-12:40"
        self.assertEqual(expected, actual)

        actual = handle_input("101051865", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10), [], "test_data.csv")
        expected = False, "INGEN MATCHANDE LUNCHTID"
        self.assertEqual(expected, actual)

        actual = handle_input("123456788", tags, times, datetime.datetime(2020, 11, 11, 12, 10, 10), [], "test_data.csv")
        expected = False, "OKÄND NYCKELTAGG"
        self.assertEqual(expected, actual)

        actual = handle_input("259648828", tags, times, datetime.datetime(2020, 11, 14, 12, 10, 10), [], "test_data.csv")
        expected = False, "DIN LUNCHTID ÄR 00:00-00:00"
        self.assertEqual(expected, actual)

    def test_correct_time(self):
        # On time for lunch
        correct_time = valid_lunch_time(["TE4", "12:10-12:30", "12:10-12:30", "12:10-12:30", "12:30-12:50", "12:30-12:50"], datetime.datetime(2020, 11, 11, 12, 10, 10))
        # 1 minute before lunch time
        wrong_before_1min = valid_lunch_time(["TE4", "12:10-12:30", "12:10-12:30", "12:10-12:30", "12:30-12:50", "12:30-12:50"], datetime.datetime(2020, 11, 11, 12, 9, 10))
        # 1 minute after lunch time
        wrong_after_1min = valid_lunch_time(["TE4", "12:10-12:30", "12:10-12:30", "12:10-12:30", "12:30-12:50", "12:30-12:50"], datetime.datetime(2020, 11, 11, 12, 9, 10))
        # Midnight
        wrong_time_midnight = valid_lunch_time(["TE4", "12:10-12:30", "12:10-12:30", "12:10-12:30", "12:30-12:50", "12:30-12:50"], datetime.datetime(2020, 11, 11, 0, 0, 1))
        # Weekend
        wrong_time_weekend = valid_lunch_time(["TE4", "12:10-12:30", "12:10-12:30", "12:10-12:30", "12:30-12:50", "12:30-12:50"], datetime.datetime(2020, 11, 14, 16, 0, 1))

        self.assertEqual(True, correct_time)
        self.assertEqual(False, wrong_before_1min)
        self.assertEqual(False, wrong_after_1min)
        self.assertEqual(False, wrong_time_midnight)
        self.assertEqual(False, wrong_time_weekend)


if __name__ == '__main__':

    args = [sys.executable, "lunchpad.py", "-test", "--csv", "test_data.csv"]

    file = os.path.dirname(os.path.realpath(__file__))

    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

    tags = get_file_data(file+"/id_tester.csv", "tags")
    times = get_file_data(file+"/tider_tester.csv", "times")

    tests = [
        ["12348910", "OKÄND NYCKELTAGG"],
        ["548381316", "GODKÄND SKANNING! SMAKLIG MÅLTID!"],
        ["548381316", "DU HAR REDAN SKANNAT"]
    ]

    unittest.main()
