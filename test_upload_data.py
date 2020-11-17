import gspread, csv, os

gc = gspread.service_account()
sh = gc.open_by_key("11V4KfT00lrys2zHgLtRlF13q3SP-6n1CS_vbCyLmtqA")
temp_filename = "temp_csv.csv"

with open(temp_filename, 'w', newline='') as f:
    writer = csv.writer(f)
    worksheet = sh.worksheet("Lunchsystem")
    writer.writerows(worksheet.get_all_values())

test_content = open("upload_data_test.csv", "r").read()
gc.import_csv(sh.id, test_content.encode("utf8"))

worksheet_value = worksheet.get_all_values()
expected_result = list(map(lambda x: x.split(","), test_content.split("\n")))

if worksheet_value == expected_result:
    print("\u001b[32mTest successful\u001b[0m")
else:
    print("\u001b[31mTest failed\u001b[0m")

real_content = open(temp_filename, "r").read().encode("utf8")
gc.import_csv(sh.id, real_content)

os.remove(temp_filename)