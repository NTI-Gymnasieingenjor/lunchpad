#!/usr/bin/env python3
import os, time, datetime
from lunchpad import *

def test_students_eaten_saved(tags_to_blipp, nti_eaten, procivitas_eaten, date):
    for tag in tags_to_blipp:
        handle_input(tag, tagsfile, timesfile, date, [])

    try:
        with open(filename, "r") as f:
            f.readline() # Reads first line and does nothing with it.
            line = f.readline()
            data_date, nti, procivitas = line.split(",")
            if nti.rstrip() == nti_eaten and procivitas.rstrip() == procivitas_eaten:
                if data_date == date.strftime('%Y-%m-%d'):
                    print("\u001b[32mTest successful\u001b[0m")
                else:
                    print("\u001b[31mTest failed\u001b[0m")
                    print("Wrong date")
            else:
                print("\u001b[31mTest failed\u001b[0m")
    except Exception as err:
        print("\u001b[31mTest failed\u001b[0m")

    # Resets the lunch_data.csv
    os.remove(filename)


if __name__ == "__main__":
    valid_tags = ["***REMOVED***", "***REMOVED***"]
    nti_tag = "***REMOVED***"
    procivitas_tag = "123456789"

    filename = "lunch_data.csv"

    file = os.path.dirname(os.path.realpath(__file__))
    tagsfile = get_file_data(file+"/id_tester.csv", "tags")
    timesfile = get_file_data(file+"/tider_tester.csv", "times")

    print("[*] Testing with 1 green tag from NTI")
    test_students_eaten_saved([nti_tag], "1", "0", datetime.datetime.today())

    print("[*] Testing with 2 green tag from NTI")
    test_students_eaten_saved(valid_tags, "2", "0", datetime.datetime.today())

    print("[*] Testing with 1 green tag from NTI and 1 green tag from PROCIVITAS")
    test_students_eaten_saved([nti_tag, procivitas_tag], "1", "1", datetime.datetime.today())

    print("[*] Testing with 1 green tag from NTI on date 2020-12-24")
    test_students_eaten_saved([nti_tag], "1", "0", datetime.datetime(2020, 12, 24, 12, 10, 10))
