from flask import Flask, render_template, jsonify
import csv
import glob
import time
import threading
from collections import deque

app = Flask(__name__)

# 创建一个全局变量来存储最新数据
latest_data = []

# 从CSV文件中读取数据的函数
def read_csv_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

        return data

# 定义一个函数用于周期性地更新数据
def update_data_periodically():
    global latest_data
    while True:
        file_paths = glob.glob('/Users/yangcong/PycharmProjects/Perf/R/_192.168.10.77:9999/results/com.yangcong345.android.phone/*/cpuinfo.csv')
        if file_paths:
            selected_file_path = file_paths[0]
            latest_data = read_csv_data(selected_file_path)
        time.sleep(5)  # 每隔5秒更新一次数据

@app.route('/')
def index():
    # 返回index.html模板，并传入latest_data作为模板参数
    return render_template('index.html', data=latest_data)

@app.route('/get_all_data')
def get_new_data():
    global latest_data
    all_data = jsonify(latest_data)
    latest_data = []  # Clear the latest_data after returning it
    return all_data

# @app.route('/get_all_data')
# def get_all_data():
#     global latest_data
#     all_data = jsonify(latest_data)
#     latest_data = []  # Clear the latest_data after returning it
#     return all_data

if __name__ == "__main__":
    # 启动一个线程周期性地更新数据
    data_update_thread = threading.Thread(target=update_data_periodically)
    data_update_thread.daemon = True
    data_update_thread.start()

    app.debug = True
    app.run(host='127.0.0.1', port=9990)
