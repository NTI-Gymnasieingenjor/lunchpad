#!/usr/bin/env python3
from datetime import datetime
from sys import executable
from os import path
import unittest
from lunchpad import handle_input, valid_lunch_time, get_file_data


class TestLunchpad(unittest.TestCase):

    def test_correct_text(self):
        """
        Test for the handle_input function. Asserts the return bool and message from handle_input and the expected.
        """
        
        # Scanned tag is on time, NTI tag
        actual = handle_input("900865598", tags, times, datetime(2020, 11, 11, 12, 10, 10), [], "test_data.csv")
        expected = True, "GODKÄND SKANNING! SMAKLIG MÅLTID!"
        self.assertEqual(expected, actual)

        # Scanned tag is on time, Procivitas tag
        actual = handle_input("739341266", tags, times, datetime(2020, 11, 11, 12, 20, 10), [], "test_data.csv")
        expected = True, "GODKÄND SKANNING! SMAKLIG MÅLTID!"
        self.assertEqual(expected, actual)

        # Scanned tag is first in list
        actual = handle_input("900865598", tags, times, datetime(2020, 11, 11, 12, 10, 10), ["78b70d2dec5594fe350af13afd2ec839695442053013ec3e2d7386429b5764b4", "2711ec7bebeff204b1d6d39cc8dcbfbef44d93da919befb9834a839d98a5e1bf"], "test_data.csv")
        expected = False, "DU HAR REDAN SKANNAT"
        self.assertEqual(expected, actual)

        # Scanned tag is last in list
        actual = handle_input("900865598", tags, times, datetime(2020, 11, 11, 12, 10, 10), ["2711ec7bebeff204b1d6d39cc8dcbfbef44d93da919befb9834a839d98a5e1bf", "78b70d2dec5594fe350af13afd2ec839695442053013ec3e2d7386429b5764b4"], "test_data.csv")
        expected = False, "DU HAR REDAN SKANNAT"
        self.assertEqual(expected, actual)

        # Scanned tag is in the middle of the list
        actual = handle_input("900865598", tags, times, datetime(2020, 11, 11, 12, 10, 10), ["2711ec7bebeff204b1d6d39cc8dcbfbef44d93da919befb9834a839d98a5e1bf", "78b70d2dec5594fe350af13afd2ec839695442053013ec3e2d7386429b5764b4", "1514aa8277131f9dc6c69f615fae6e15cce2022237a5c98a3533f2007bb99aba"], "test_data.csv")
        expected = False, "DU HAR REDAN SKANNAT"
        self.assertEqual(expected, actual)

        # Scanned tag is off time, NTI tag
        actual = handle_input("754729301", tags, times, datetime(2020, 11, 11, 12, 10, 10), [], "test_data.csv")
        expected = False, "DIN LUNCHTID ÄR 11:00-11:20"
        self.assertEqual(expected, actual)

        # Scanned tag is off time, Procivitas tag
        actual = handle_input("739341266", tags, times, datetime(2020, 11, 11, 12, 10, 10), [], "test_data.csv")
        expected = False, "DIN LUNCHTID ÄR 12:20-12:40"
        self.assertEqual(expected, actual)

        actual = handle_input("101051865", tags, times, datetime(2020, 11, 11, 12, 10, 10), [], "test_data.csv")
        expected = False, "INGEN MATCHANDE LUNCHTID"
        self.assertEqual(expected, actual)

        actual = handle_input("123456788", tags, times, datetime(2020, 11, 11, 12, 10, 10), [], "test_data.csv")
        expected = False, "OKÄND NYCKELTAGG"
        self.assertEqual(expected, actual)

        actual = handle_input("259648828", tags, times, datetime(2020, 11, 14, 12, 10, 10), [], "test_data.csv")
        expected = False, "DIN LUNCHTID ÄR 00:00-00:00"
        self.assertEqual(expected, actual)

    def test_correct_time(self):
        """
        Test for the valid_lunch_time function. Asserts the bool value from valid_lunch_time function and expected bool value.
        """
        # On time for lunch
        correct_time = valid_lunch_time(["TE4", "12:10-12:30", "12:10-12:30", "12:10-12:30", "12:30-12:50", "12:30-12:50"], datetime(2020, 11, 11, 12, 10, 10))
        # 1 minute before lunch time
        wrong_before_1min = valid_lunch_time(["TE4", "12:10-12:30", "12:10-12:30", "12:10-12:30", "12:30-12:50", "12:30-12:50"], datetime(2020, 11, 11, 12, 9, 10))
        # 1 minute after lunch time
        wrong_after_1min = valid_lunch_time(["TE4", "12:10-12:30", "12:10-12:30", "12:10-12:30", "12:30-12:50", "12:30-12:50"], datetime(2020, 11, 11, 12, 9, 10))
        # Midnight
        wrong_time_midnight = valid_lunch_time(["TE4", "12:10-12:30", "12:10-12:30", "12:10-12:30", "12:30-12:50", "12:30-12:50"], datetime(2020, 11, 11, 0, 0, 1))
        # Weekend
        wrong_time_weekend = valid_lunch_time(["TE4", "12:10-12:30", "12:10-12:30", "12:10-12:30", "12:30-12:50", "12:30-12:50"], datetime(2020, 11, 14, 16, 0, 1))

        self.assertEqual(True, correct_time)
        self.assertEqual(False, wrong_before_1min)
        self.assertEqual(False, wrong_after_1min)
        self.assertEqual(False, wrong_time_midnight)
        self.assertEqual(False, wrong_time_weekend)


if __name__ == '__main__':

    args = [executable, "lunchpad.py", "--tags", "id_tester.csv", "--schedule", "tider_tester.csv", "--data", "test_data.csv"]

    file = path.dirname(path.realpath(__file__))

    tags = get_file_data(file+"/id_tester.csv")
    times = get_file_data(file+"/tider_tester.csv")

    unittest.main()
