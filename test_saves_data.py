#!/usr/bin/env python3
import os
import time
import datetime
from lunchpad import *


def test_students_eaten_saved(tags_to_blipp, nti_eaten, procivitas_eaten, date):
    """
    The function resets the lunch_data csv file and asserts the actual amount of students that have eaten with the expected amount.
    """

    # Resets the lunch_data.csv
    if os.path.isfile(filename):
        os.remove(filename)

    global failed
    for tag in tags_to_blipp:
        handle_input(tag, tagsfile, timesfile, date, [], filename)

    try:
        with open(filename, "r") as f:
            data = f.readlines()
            data_date, nti, procivitas = data[1].split(",")
            if nti.rstrip() == nti_eaten and procivitas.rstrip() == procivitas_eaten:
                if data_date == date.strftime('%Y-%m-%d'):
                    print("\u001b[32mTest successful\u001b[0m")
                else:
                    print("\u001b[31mTest failed\u001b[0m")
                    failed = True
                    print("Wrong date")
            else:
                print("\u001b[31mTest failed\u001b[0m")
                failed = True
    except Exception as err:
        print("\u001b[31mTest failed\u001b[0m")
        failed = True



def test_students_eaten_append(tag, nti_eaten, procivitas_eaten, dates, expected_data):
    """
    Test by asserting that actual is not equal to expected. The test tests with green tags from different dates.
    This is to test that the function appends to a new line on a new date.
    """

    global failed

    if os.path.isfile(filename):
        os.remove(filename)

    for date in dates:
        handle_input(tag, tagsfile, timesfile, date, [], filename)

    actual_data = None
    with open(filename, "r") as f:
        actual_data = f.readlines()

    if actual_data != expected_data:
        print("\u001b[32mTest successful\u001b[0m")
    else:
        print("\u001b[31mTest failed\u001b[0m")
        failed = True


if __name__ == "__main__":
    failed = False
    valid_tags = ["548381316", "900865598"]
    nti_tag = "548381316"
    procivitas_tag = "123456789"
    filename = "test_data.csv"

    file = os.path.dirname(os.path.realpath(__file__))
    tagsfile = get_file_data(file+"/id_tester.csv")
    timesfile = get_file_data(file+"/tider_tester.csv")

    print("[*] Testing with 1 green tag from NTI")
    test_students_eaten_saved([nti_tag], "1", "0", datetime.datetime.now())

    print("[*] Testing with 2 green tag from NTI")
    test_students_eaten_saved(valid_tags, "2", "0", datetime.datetime.now())

    print("[*] Testing with 1 green tag from NTI and 1 green tag from PROCIVITAS")
    test_students_eaten_saved([nti_tag, procivitas_tag], "1", "1", datetime.datetime.now())

    print("[*] Testing with 1 green tag from NTI on date 2020-12-24")
    test_students_eaten_saved([nti_tag], "1", "0", datetime.datetime(2020, 12, 24, 12, 10, 10))

    print("[*] Testing with 1 green tag one date then 1 green tag another date")
    expected_data = ["DATUM,NTI,PROCIVITAS\n", "2020-11-10,1,0\n", "2020-11-11,1,0\n"]
    dates = [datetime.datetime(2020, 11, 10, 12, 10, 10), datetime.datetime(2020, 11, 11, 12, 10, 10)]
    test_students_eaten_append(nti_tag, "1", "0", dates, expected_data)

    if os.path.isfile(filename):
        os.remove(filename)

    if failed:
        sys.exit(1)
