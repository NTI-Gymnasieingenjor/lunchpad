#!/usr/bin/python3
"""
Downloads CSV files
"""
import csv
import gspread
from google.auth.exceptions import TransportError


def download_sheets_data(sheets_id, filename):
    """
    Downloads data from specified sheet into specified filename
    """
    sheet = gc.open_by_key(sheets_id)
    worksheet = sheet.get_worksheet(0)
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(worksheet.get_all_values())


if __name__ == "__main__":
    try:
        gc = gspread.service_account()
        print("[*] Downloading specialcase CSV file")
        download_sheets_data("1lEY7VggOL4xzkbppKcxsn9U5sn0nJTJzExsR12MkxpI", "specialcases.csv")
    except TransportError:
        print("\u001b[31mTimed out:\n   Retry. Try connecting to another network if not working.\u001b[0m")
    except Exception as err:
        print(err)
