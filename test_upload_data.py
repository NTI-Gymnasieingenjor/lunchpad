import subprocess, gspread, os, sys

def check_data():
    """
    Checks if Google Sheets is updated with the correct data.
    """
    global test_filename
    worksheet_value = worksheet.get_all_values()
    test_content = open(test_filename, "r").read()
    test_content_list = test_content.split("\n")
    test_content_list = list(filter(lambda elem: elem != "", test_content_list))
    expected_result = list(map(lambda x: x.split(","), test_content_list))
    expected_result = list(filter(lambda elem: elem != "", expected_result))
    if expected_result == worksheet_value:
        print("\u001b[32mTest successful\u001b[0m")
    else:
        print("\u001b[31mTest failed\u001b[0m")

gc = gspread.service_account()
sh = gc.open_by_key("11V4KfT00lrys2zHgLtRlF13q3SP-6n1CS_vbCyLmtqA")

worksheet_title = "TEST"

worksheet = sh.add_worksheet(title=worksheet_title, rows="10", cols="10")

test_filename = "test_data.csv"

with open(test_filename, "w") as fd:
    data = ["DATUM,NTI,PROCIVITAS\n", "2020-11-12,20,20\n", "2020-11-13,50,60\n", "2020-11-15,100,60\n"]
    fd.writelines(data)

args = [sys.executable, "upload_data.py", "--csv", test_filename, "--worksheet", worksheet_title]
p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
p.communicate()

# If the exit code from the subprocess does not equal 0
if p.returncode:
    print("\u001b[31mTest failed\u001b[0m")
else:
    check_data()

sh.del_worksheet(worksheet)
os.remove(test_filename)
