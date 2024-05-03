import csv
import io
import sys
import os
import chardet
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
fileData = os.path.join(current_dir, "data.csv")
fileResult = os.path.join(current_dir, "result.csv")


with open(fileData, "rb") as file:
    raw_data = file.read()
    encoding_result = chardet.detect(raw_data)

    file.seek(0)
    csv_reader = csv.reader(io.TextIOWrapper(file, encoding=encoding_result["encoding"]), delimiter="\t", dialect="excel", lineterminator="\r\n")
    csv_Header = next(csv_reader)  # Read the header row
    
    if os.path.exists(fileResult):
        os.remove(fileResult)

    # Count the total number of rows
    num_rows = sum(1 for _ in csv_reader)

    # Reset file pointer to beginning
    file.seek(0)

    columnName = "DP_NIM060_01.T_ISSUE_INFO"

    with open(fileResult, "w", newline="", encoding=encoding_result["encoding"]) as csvfile:
        csvfile.write("INSERT INTO " + columnName + " (\n\t")
        csvfile.write("\n\t,".join(csv_Header)) 
        csvfile.write("\n)\n")
        csvfile.write("SELECT\n\t")
        
        # Skip the first row
        next(csv_reader)
        for row_idx, row in enumerate(csv_reader):
            encoded_row = [str(cell) for cell in row]
            for data_idx, data in enumerate(encoded_row):
                if data.strip() == "« NULL »" or data.strip() == "":
                    cleaned_part = "null\n"
                else:
                    cleaned_part = "'"+data.strip()+"'\n"
                if re.match(r"\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}", data.strip()) or re.match(r"\d{4}/\d{2}/\d{2} \d{1}:\d{2}:\d{2}", data.strip()):
                    cleaned_part = "TO_DATE('" + data.strip() + "', 'yyyy/mm/dd hh24:mi:ss')\n"
                elif re.match(r"\d{4}/\d{2}/\d{2}", data.strip()):
                    cleaned_part = "TO_DATE('" + data.strip() + "', 'yyyy/mm/dd')\n"      
                csvfile.write(cleaned_part)
                if data_idx != len(encoded_row) - 1:
                    csvfile.write("\t,")
            if row_idx == num_rows - 1:
                csvfile.write("FROM\n\tdual;")
            else:
                csvfile.write("FROM\n\tdual\nUNION ALL\nSELECT\n\t")
