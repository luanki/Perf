from flask import Flask, jsonify, render_template
import csv
import glob
import time
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
latest_data = []  # Create a global variable to store the latest data

# Function to parse CSV data and update the latest_data variable
def update_data_from_csv():
    global latest_data
    while True:
        file_paths = glob.glob('/Users/yangcong/PycharmProjects/Perf/R/_192.168.10.77:9999/results/com.yangcong345.android.phone/*/cpuinfo.csv')  # Replace with the actual path to your CSV files
        if file_paths:
            selected_file_path = file_paths[0]
            with open(selected_file_path, 'r') as file:
                reader = csv.DictReader(file)
                latest_data = list(reader)
        time.sleep(5)  # Update the data every 5 seconds


# Endpoint to retrieve the parsed data
@app.route('/get_all_data')  # Ensure that the route accepts GET requests
def get_all_data():
    global latest_data
    return jsonify(latest_data)

# 用于呈现 index.html 页面的路由
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    # Start a thread to update data from CSV files periodically
    data_update_thread = threading.Thread(target=update_data_from_csv)
    data_update_thread.daemon = True
    data_update_thread.start()

    app.debug = True
    app.run(host='127.0.0.1', port=9900)
