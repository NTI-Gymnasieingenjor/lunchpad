# Lunchpad
A system for making sure students eat at their correct lunch time, using NFC scanning.

The goal of this system is to prevent spread of covid-19, as well as reduce the amount of food that is thrown away by keeping data on how many people eat each day.

# Definition of Done
+ Tests must pass.
+ Code must be commented.
+ No commented-out code.
+ Code and documentation must be uploaded and be up to date on GitHub.
+ Code should follow the coding conventions in place.

# Before merging with main
+ All code and documentation should be read by groupmembers onsite and approved.

# Coding Standard

**File name structure:** example_file_name (snake_case)

**Variables/Classes/Functions:** Same as file names

# Creating a Google API Service Account

The code for Lunchpad saves the data of how many people have successfully scanned each day. For uploading this data to Google Spreadsheets, we use a Google API Service Account connected to the Raspberry Pi.

[Here](https://docs.google.com/document/d/1Fhw4WIC9lVZuAJ3NJjE2ZAt_Lwe_UcJcmD8Hc1QBknc) is our guide on how to create a Google API Service Account, create a key from that service account, and use that service account key with the [gspread API](https://gspread.readthedocs.io/en/latest/index.html)

# Setup guide


### Follow the documentation <a href="/documentation.md">here</a>.

# Raspberry pi credentials
https://docs.google.com/document/d/1uhNkTdPoOy71JWvDgdG-ppMmyD-SrDYEeLO8v2bo4ZY/edit?usp=sharing
