from flask import Flask, request, render_template, redirect, url_for, session,json
import subprocess
import os
from datetime import datetime
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    csv_content = session.get('csv_content')
    selected_tool = session.get('selected_tool')
    csv_data = session.get('csv_data')
    return render_template('index.html', csv_content=csv_content, selected_tool=selected_tool, csv_data=csv_data)

@app.route('/write-note', methods=['GET', 'POST'])
def write_note_page():
    csv_content = get_csv_content()
    return render_template('writeNote.html',csv_content=csv_content)

@app.route('/write-note/write', methods=['POST'])
def write_note():
    # Get form data
    note = request.form.get('note')
    name = request.form.get('name')
    no = request.form.get('name')
    fd=request.form.get('fd')
    ud= request.form.get('ud')

    # Check if note or name is empty
    if not note:
        error_message = "Note are required fields."
        csv_content = get_csv_content()
        return render_template('writeNote.html', error_message=error_message,note=note, name=name,no=no, fd=fd,ud=ud,csv_content=csv_content)
    if not name:
        error_message = "Name are required fields."
        csv_content = get_csv_content()
        return render_template('writeNote.html', error_message=error_message,note=note, name=name,no=no, fd=fd,ud=ud,csv_content=csv_content)
    else:    
        data={
            "note" : request.form.get('note'),
            "no" : request.form.get('no'),
            "name" : request.form.get('name'),
            "fd" : request.form.get('fd').splitlines(),
            "ud" : request.form.get('ud').splitlines(),
        }
        
        json_data = json.dumps(data)
        tool_name = "writeNote.py"
        tool_path = find_tool(tool_name)
        if tool_path is None:
            return "Tool not found."  
        else:
            result = subprocess.run(['python', tool_path],input=json_data  , capture_output=True, text=True)
            csv_content = get_csv_content()
            return redirect(url_for('write_note_page'))

def get_csv_content():
    data_directory = "./notes/data"
    current_date = datetime.now()
    current_year = str(current_date.year)
    current_month = str(current_date.month).zfill(2)
    current_day = str(current_date.day).zfill(2)
    current_month_eng = current_date.strftime("%B")

    year_directory = os.path.join(data_directory, current_year)
    month_directory = os.path.join(year_directory, current_month_eng)
    csv_filename = os.path.join(month_directory, f"{current_day}-{current_month}.csv")

    if os.path.exists(csv_filename) and os.path.isfile(csv_filename):
        with open(csv_filename, 'r', newline='', encoding='utf-8') as file:
            csv_content = file.read()
        return csv_content
    else:
        return ""



@app.route('/write-csv/format', methods=['POST'])
def write_csv_format():
    global csv_content, selected_tool, csv_data
    
    csv_data = request.form.get('csv_data', '')
    if csv_data:
        file_path = os.path.join(os.path.abspath('.'), 'createSelectSQL', 'data.csv')
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            file.write(csv_data)
    
    if not csv_data:
        csv_data = ""
    
    tool_name = "format.py"
    tool_path = find_tool(tool_name)
    if tool_path:
        result = subprocess.run(['python', tool_path], capture_output=True, text=True)
        if result.returncode == 0:
            tool_dir = os.path.dirname(tool_path)
            csv_file_path = os.path.join(tool_dir, 'result.csv')
            csv_content = read_csv_file(csv_file_path)
            selected_tool = tool_name
            
            return redirect(url_for('write_csv_format_home'))
        else:
            return "Error occurred while running the tool."
    else:
        return "Tool not found."

@app.route('/write-csv', methods=['GET', 'POST'])
def write_csv_format_home():
    tool_name = "format.py"
    tool_path = find_tool(tool_name)
    if tool_path:
        result = subprocess.run(['python', tool_path], capture_output=True, text=True)
        if result.returncode == 0:
            tool_dir = os.path.dirname(tool_path)
            csv_file_path = os.path.join(tool_dir, 'result.csv')
            csv_content = read_csv_file(csv_file_path)
            selected_tool = tool_name
    return render_template('index.html', csv_content=csv_content, selected_tool=selected_tool, csv_data=csv_data)
      


@app.route('/write-csv-i/index', methods=['POST'])
def write_csv_index():
    global csv_content, selected_tool, csv_data
    
    csv_data = request.form.get('csv_data', '')
    if csv_data:
        file_path = os.path.join(os.path.abspath('.'), 'createRedmine', 'data.csv')
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            file.write(csv_data)
    
    if not csv_data:
        csv_data = ""
    
    tool_name = "index.py"
    tool_path = find_tool(tool_name)
    if tool_path:
        result = subprocess.run(['python', tool_path], capture_output=True, text=True)
        if result.returncode == 0:
            tool_dir = os.path.dirname(tool_path)
            csv_file_path = os.path.join(tool_dir, 'result.csv')
            csv_content = read_csv_file(csv_file_path)
            selected_tool = tool_name
            
            return redirect(url_for('write_csv_index_home'))
        else:
            return "Error occurred while running the tool."
    else:
        return "Tool not found."

@app.route('/write-csv-i', methods=['GET', 'POST'])
def write_csv_index_home():
    tool_name = "index.py"
    tool_path = find_tool(tool_name)
    if tool_path:
        result = subprocess.run(['python', tool_path], capture_output=True, text=True)
        if result.returncode == 0:
            tool_dir = os.path.dirname(tool_path)
            csv_file_path = os.path.join(tool_dir, 'result.csv')
            csv_content = read_csv_file(csv_file_path)
            selected_tool = tool_name
    return render_template('index.html', csv_content=csv_content, selected_tool=selected_tool, csv_data=csv_data)




def find_tool(tool_name):
    current_dir = os.path.abspath('.')
    target_dirs = [os.path.join(current_dir, 'createSelectSQL'), os.path.join(current_dir, 'createRedmine'), os.path.join(current_dir, 'notes')]
    for target_dir in target_dirs:
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file == tool_name:
                    return os.path.join(root, file)
    return None

def read_csv_file(csv_file_path):
    csv_content = ''
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_content = file.read()
    return csv_content

if __name__ == '__main__':
    app.run(debug=True)
