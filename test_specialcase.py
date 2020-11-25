#!/usr/bin/python3
"""
 Tests the specialcase feature
"""
import os
import sys
import datetime
from lunchpad import *


def create_test_specialcases_file():
    """
    Creates the specialcases test file
    """
    data = ["MFR,Monday,Tuesday,Wednesday,Thursday,Friday\n",
            "548381316,10:00-14:00,,,,\n",
            "617153648,,,10:00-14:00,,\n"]

    with open(SPECIALCASE_FILENAME, "w") as f:
        f.writelines(data)

def test_tag_in_specialcase(tag, expected):
    """
    Tests for correct output if tag in specialcase
    """
    global failed
    result = get_specialcase_times(tag, SPECIALCASE_FILENAME)
    if result == expected:
        print("\u001b[32mTEST COMPETE\u001b[0m")
    else:

        print("\u001b[31mTEST FAILED\u001b[0m")
        failed = True



def test_specialcase(tag, date, expected):
    """
    Tests for correct output if tag in specialcase
    and correct weekday
    """

    global failed
    res = handle_input(tag, tag_times, date, [], DATA_FILENAME, SPECIALCASE_FILENAME)


    if res == expected:
        print("\u001b[32mTEST COMPETE\u001b[0m")
    else:

        print("\u001b[31mTEST FAILED\u001b[0m")
        failed = True



if __name__ == "__main__":
    failed = False
    DATA_FILENAME = "test_data.csv"
    SPECIALCASE_FILENAME = "test_specialcases.csv"
    PATH = os.path.dirname(os.path.realpath(__file__))
    tag_times = get_file_data(PATH+"/tag_time_tests.csv")

    TAGS_WITH_SPECIALCASE = ["548381316", "617153648"]
    NO_SPECIALCASE_TAG = "611056439"

    # Creates the specialcase test file
    create_test_specialcases_file()

    print("[*] Testing with tag in specialcase csv")
    test_tag_in_specialcase(TAGS_WITH_SPECIALCASE[0], ["SPECIALCASE", "10:00-14:00", "", "", "", ""])

    print("[*] Testing with tag not in specialcase csv")
    test_tag_in_specialcase(NO_SPECIALCASE_TAG, [])

    print("[*] Testing with tag with specialcase on monday at wrong time")
    expected_result = False, "DIN LUNCHTID ÄR 10:00-14:00"
    test_date = datetime.datetime(2020, 11, 23, 15, 10, 10)
    test_specialcase(TAGS_WITH_SPECIALCASE[0], test_date, expected_result)

    print("[*] Testing with tag with specialcase on wednesday at wrong time")
    expected_result = False, "DIN LUNCHTID ÄR 10:00-14:00"
    test_date = datetime.datetime(2020, 11, 25, 15, 10, 10)
    test_specialcase(TAGS_WITH_SPECIALCASE[1], test_date, expected_result)

    print("[*] Testing with tag with specialcase on monday at correct time")
    expected_result = True, "GODKÄND SKANNING! SMAKLIG MÅLTID!"
    test_date = datetime.datetime(2020, 11, 23, 13, 10, 10)
    test_specialcase(TAGS_WITH_SPECIALCASE[0], test_date, expected_result)

    print("[*] Testing with tag with specialcase on wednesday at correct time")
    expected_result = True, "GODKÄND SKANNING! SMAKLIG MÅLTID!"
    test_date = datetime.datetime(2020, 11, 25, 13, 10, 10)
    test_specialcase(TAGS_WITH_SPECIALCASE[1], test_date, expected_result)

    print("[*] Testing with tag without specialcase for tuesday")
    expected_result = False, "DIN LUNCHTID ÄR 12:30-12:50"
    test_date = datetime.datetime(2020, 11, 24, 13, 10, 10)
    test_specialcase(TAGS_WITH_SPECIALCASE[1], test_date, expected_result)

    if failed:
        sys.exit(1)
    # Removes the specialcase test file
    os.remove(SPECIALCASE_FILENAME)
