import os
import csv,json
from datetime import datetime



def write_csv(csv_filename, data):

    with open(csv_filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if data.get("no"):
            writer.writerow([data["note"] + "#note-" + data["no"]])
        else:
            writer.writerow([data["note"]])
        writer.writerow([data["name"]])
        file.write("\n") 
        if data.get("fd"):
            writer.writerow(["fd:"])
            for fd_item in data["fd"]:
                file.write("\t")
                writer.writerow([fd_item])
            file.write("\n")  
        if data.get("ud"):
            writer.writerow(["ud:"])
            for ud_item in data["ud"]:
                file.write("\t")
                writer.writerow([ud_item]) 
        file.write("\n\n            -----------------------------------------------------------------------------\n\n")

    with open(sum_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        file.write(current_date_fileSum) 
        file.write("\n") 
        if data.get("no"):
            writer.writerow([data["note"] + "#note-" + data["no"]])
        else:
            writer.writerow([data["note"]])
        writer.writerow([data["name"]])
        file.write("\n") 
        if data.get("fd"):
            writer.writerow(["fd:"])
            for fd_item in data["fd"]:
                file.write("\t")
                writer.writerow([fd_item])
            file.write("\n")  
        if data.get("ud"):
            writer.writerow(["ud:"])
            for ud_item in data["ud"]:
                file.write("\t")
                writer.writerow([ud_item]) 
        file.write("\n\n            -----------------------------------------------------------------------------\n\n") 
        
current_dir = os.path.dirname(os.path.abspath(__file__))

sum_file = os.path.join(current_dir, "all-note.csv")

data_input = input()


data = json.loads(data_input)


current_file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(current_file_path)
data_directory = os.path.join(current_directory, "data")

current_date = datetime.now()
current_date_fileSum = datetime.now().strftime('%Y/%m/%d')
current_year = str(current_date.year)
current_day = str(current_date.day).zfill(2)
current_month = str(current_date.month).zfill(2)
current_month_eng = current_date.strftime("%B")

year_directory = os.path.join(data_directory, current_year)

if not os.path.exists(year_directory):
    os.makedirs(year_directory)

month_directory = os.path.join(year_directory, current_month_eng)
if not os.path.exists(month_directory):
    os.makedirs(month_directory)


csv_filename = os.path.join(month_directory, f"{current_day}-{current_month}.csv")
if not os.path.exists(csv_filename):
    with open(csv_filename, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
    write_csv(csv_filename, data)
else:
    write_csv(csv_filename, data) 