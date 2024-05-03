from flask import Flask, request, render_template, redirect, url_for, session
import subprocess
import os
app = Flask(__name__)


@app.route('/')
def home():
    csv_content = session.get('csv_content')
    selected_tool = session.get('selected_tool')
    csv_data = session.get('csv_data')
    return render_template('index.html', csv_content=csv_content, selected_tool=selected_tool, csv_data=csv_data)

# @app.route('/run-tool', methods=['POST'])
# def run_tool():
#     global csv_content, selected_tool
    
#     tool_name = request.form['tool_name']
#     tool_path = find_tool(tool_name)
#     if tool_path:
#         result = subprocess.run(['python', tool_path], capture_output=True, text=True)
#         tool_dir = os.path.dirname(tool_path)
#         csv_file_path = os.path.join(tool_dir, 'result.csv')
#         csv_content = read_csv_file(csv_file_path)
#         selected_tool = tool_name
#         return redirect(url_for('home'))
#     else:
#         return "Tool not found."

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
            
            return render_template('index.html', csv_content=csv_content, selected_tool=selected_tool, csv_data=csv_data)
        else:
            return "Error occurred while running the tool."
    else:
        return "Tool not found."


@app.route('/write-csv/index', methods=['POST'])
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
            
            return render_template('index.html', csv_content=csv_content, selected_tool=selected_tool, csv_data=csv_data)
        else:
            return "Error occurred while running the tool."
    else:
        return "Tool not found."





def find_tool(tool_name):
    current_dir = os.path.abspath('.')
    target_dirs = [os.path.join(current_dir, 'createSelectSQL'), os.path.join(current_dir, 'createRedmine')]
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
    app.run()
