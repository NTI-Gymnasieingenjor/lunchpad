#!/usr/bin/env python3
import gspread
import sys
import os
import argparse
from google.auth.exceptions import *
from datetime import datetime


def sort_data(data):
    headings = data.pop(data.index("DATUM,NTI,PROCIVITAS,NTI_TEACHER,PROCIVITAS_TEACHER"))
    sorted_data = sorted(data, key=lambda x: datetime.strptime(x.split(",")[0], "%Y-%m-%d"))
    sorted_data.insert(0, headings)
    return sorted_data


def upload_data(data):
    data = sort_data(data)
    try:
        for idx, row in enumerate(data):
            date, nti, procivitas, nti_teacher, procivitas_teacher = row.split(",")
            worksheet.update_cell(idx + 1, "1", date)
            worksheet.update_cell(idx + 1, "2", nti)
            worksheet.update_cell(idx + 1, "3", procivitas)
            worksheet.update_cell(idx + 1, "4", nti_teacher)
            worksheet.update_cell(idx + 1, "5", procivitas_teacher)
    except Exception as err:
        if type(err) == TransportError:
            print("\u001b[31mTimed out:\n   Retry. Try connecting to another network if not working.\u001b[0m")
        else:
            print(err)
        sys.exit(1)

def get_options(args):
    parser = argparse.ArgumentParser(description="Uploads the number of people that have scanned their tags.")

    parser.add_argument("-d", "--data", nargs='?', default=file + "/lunch_data.csv", type=argparse.FileType("r"), help="Specifies CSV file containing the lunch data.")
    parser.add_argument("-w", "--worksheet", nargs='?', default="Lunchsystem", help="Specifies name of the worksheet on Google Spreadsheets.")
    
    options = parser.parse_args(args)
    return options

if __name__ == '__main__':
    try:
        file = os.path.dirname(os.path.realpath(__file__))
        options = get_options(sys.argv[1:])
        
        # Initializes Google Sheets document.
        gc = gspread.service_account()
        sh = gc.open_by_key("11V4KfT00lrys2zHgLtRlF13q3SP-6n1CS_vbCyLmtqA")
        worksheet = sh.worksheet(options.worksheet)

        local_data = options.data.read().splitlines()

        # Close input file stream
        options.data.close()

        # Reformats sheet data to match the formatting of our local data.
        sheet_data = list(map(lambda x: ",".join(x), worksheet.get_all_values()))
        formatted_sheet_data = []
        combined_data = []
        
        # Removes all week numbers and weekdays from imported sheet data. 
        for idx, row in enumerate(sheet_data):
            if idx != 0:
                new_string = row.split(" ")[0]
                new_string += "," + row.split(",")[1]
                new_string += "," + row.split(",")[2]
                formatted_sheet_data.append(new_string)
            else:
                formatted_sheet_data.append(row)
        
        # Removed potential empty strings from local_data.
        local_data = list(filter(lambda elem: elem != "", local_data))
        combined_data = local_data + formatted_sheet_data
        unique_data = list(set(combined_data))

        upload_data(unique_data)
    except Exception as err:
        if type(err) == TransportError:
            print("\u001b[31mTimed out:\n   Retry. Try connecting to another network if not working.\u001b[0m")
        else:
            print(err)
        sys.exit(1)
