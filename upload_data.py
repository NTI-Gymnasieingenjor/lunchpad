import gspread, sys, os

from datetime import datetime

def sort_data(data):
    headings = data.pop(data.index("DATUM,NTI,PROCIVITAS"))
    sorted_data = sorted(data, key=lambda x: datetime.strptime(x.split(",")[0], "%Y-%m-%d"))
    sorted_data.insert(0, headings)
    return sorted_data

def upload_data(data):
    data = sort_data(data)
    try:
        for idx, row in enumerate(data):
            date, nti, procivitas = row.split(",")
            worksheet.update_cell(idx + 1, "1", date)
            worksheet.update_cell(idx + 1, "2", nti)
            worksheet.update_cell(idx + 1, "3", procivitas)
    except Exception as err:
        print(err)
        sys.exit(1)

if __name__ == '__main__':

    gc = gspread.service_account()
    sh = gc.open_by_key("11V4KfT00lrys2zHgLtRlF13q3SP-6n1CS_vbCyLmtqA")
    worksheet = sh.worksheet("Lunchsystem")

    data_file = "lunch_data.csv"

    if "--csv" in sys.argv:
        try:
            data_file = sys.argv[sys.argv.index("--csv") + 1] 
        except IndexError as err:
            print(err)
            print("\u001b[31mNo file was specified\u001b[0m.")
            sys.exit(1)
    
    if not os.path.isfile(data_file):
        print("\u001b[31mCould not read file: {}\u001b[0m".format(data_file))
        sys.exit(1)

    if "--worksheet" in sys.argv:
        try:
            worksheet = sh.worksheet(sys.argv[sys.argv.index("--worksheet") + 1])
        except IndexError as err:
            print(err)
            print("\u001b[31mNo worksheet was specified\u001b[0m.")
            sys.exit(1)

    local_data = None
    sheet_data = list(map(lambda x: ",".join(x), worksheet.get_all_values()))
    formatted_sheet_data = []
    combined_data = []
    for idx, row in enumerate(sheet_data):
        if idx != 0:
            new_string = row.split(" ")[0]
            new_string += "," + row.split(",")[1]
            new_string += "," + row.split(",")[2]
            formatted_sheet_data.append(new_string)
        else:
            formatted_sheet_data.append(row)

    with open(data_file, 'r') as f:
        local_data = f.read().split("\n")

    
    try:
        with open(data_file, 'r') as f:
            local_data = f.read().split("\n")
    except:
        print("\u001b[31mCould not read file: {}\u001b[0m".format(data_file))
        sys.exit(1)

    local_data = list(filter(lambda elem: elem != "", local_data))
    combined_data = local_data + formatted_sheet_data
    unique_data = list(set(combined_data))


    upload_data(unique_data)
