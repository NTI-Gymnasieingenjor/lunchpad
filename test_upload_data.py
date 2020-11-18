import subprocess, gspread, os

def check_data():
    global test_filename
    gc = gspread.service_account()
    sh = gc.open_by_key("11V4KfT00lrys2zHgLtRlF13q3SP-6n1CS_vbCyLmtqA")
    worksheet = sh.worksheet("Lunchsystem")
    worksheet_value = worksheet.get_all_values()
    test_content = open(test_filename, "r").read()
    expected_result = list(map(lambda x: x.split(","), test_content.split("\n")))

    if expected_result in worksheet_value:
        print("\u001b[32mTest successful\u001b[0m")
    else:
        print("\u001b[31mTest failed\u001b[0m")

    old_content = open("temp_old_data.csv", "r").read()
    gc.import_csv(sh.id, old_content.encode("utf8"))
    os.remove("temp_old_data.csv")

test_filename = "upload_data_test.csv"

args = ["python3", "upload_data.py", "--csv", test_filename, "--test"]
p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

res = p.stdout.readline().decode("latin-1").strip()
expected_res = "Upload complete."

if res == expected_res:
    check_data()
else:
    print("\u001b[31mTest failed\u001b[0m")
