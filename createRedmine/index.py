import chardet
import re
import os

# Đường dẫn của thư mục hiện tại
current_dir = os.path.dirname(os.path.abspath(__file__))

# Tạo đường dẫn tới file CSV từ thư mục hiện tại
input_file = os.path.join(current_dir, "data.csv")
output_file = os.path.join(current_dir,"result.csv")

# Detect the encoding of the input file
with open(input_file, "rb") as file:
    raw_data = file.read()
    encoding_result = chardet.detect(raw_data)

# Updated dictionary structure
sections = {"Implement": {"fd": [], "ud": []}, "Updated": {"fd": [], "ud": []}}

# Read the raw data line by line
with open(input_file, "r", encoding=encoding_result["encoding"]) as infile:
    for line in infile:
        line = line.strip()
        if line.endswith('i') and "fd" in line:
            sections["Implement"]["fd"].append(re.sub(r'\s+', '    ', line[:-1]))
        elif line.endswith('i') and "ud" in line:
            sections["Implement"]["ud"].append(re.sub(r'\s+', '    ', line[:-1]))
        elif line.endswith('u') and "fd" in line:
            sections["Updated"]["fd"].append(re.sub(r'\s+', '    ', line[:-1]))
        elif line.endswith('u') and "ud" in line:
            sections["Updated"]["ud"].append(re.sub(r'\s+', '    ', line[:-1]))

# Write the lines to the output file
with open(output_file, "w", encoding=encoding_result["encoding"]) as outfile:
    for section, types in sections.items():
        has_data = any(lines for lines in types.values())
        if has_data:
            outfile.write("*" + section + ":*")
            for type_, lines in types.items():
                if lines:
                    outfile.write("\n> "+type_ + ":\n<pre>\n")
                    for line in lines:
                        outfile.write(line + "\n")
                    outfile.write("</pre>")
                outfile.write("\n")

