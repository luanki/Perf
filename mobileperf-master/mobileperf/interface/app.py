from flask import Flask, request, jsonify
from flask_cors import CORS
from mobileperf.android.DB_utils import DatabaseOperations
from datetime import datetime
import pandas as pd

app = Flask(__name__)
CORS(app)
db_operations = DatabaseOperations()

# 添加自定义响应头
@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# 查看所有设备信息
@app.route('/latest_ids', methods=['GET'])
def get_devices():
    devices = db_operations.get_all_devices()
    #print(devices)
    if devices:
        devices_sorted = sorted(devices, key=lambda x: x[3], reverse=True)
        devices_dict = [
            {
                "device_id": device[0],
                "device_name": device[1],
                "model": device[2],
                "created_at": device[3].strftime("%Y-%m-%d %H:%M:%S") if isinstance(device[3], datetime) else device[3],
                "other_field": device[4]
            }
            for device in devices_sorted
        ]
        return jsonify(devices_dict)
    else:
        return jsonify({"message": "未找到设备"}), 404

# 请求对应ids的设备所有性能数据
@app.route('/view_device_perf_info', methods=['POST'])
def view_device_perf_info():
    data = request.json
    sn = data.get('device_name')
    ids = data.get('other_field')

    perf_data = db_operations.get_devices_perf_info(sn, ids)

    if perf_data is not None:
        try:
            df = pd.DataFrame(perf_data)
            date_columns = ['created_at', 'fps_datetime', 'fps_recorded_at', 'cpu_datetime', 'cpu_recorded_at',
                            'mem_datetime', 'mem_recorded_at']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')

            result = df.to_dict(orient='records')
            return jsonify(result), 200
        except Exception as e:
            print(f"Error processing data: {e}")
            return jsonify({"message": "Internal server error"}), 500
    else:
        return jsonify({"message": "未找到设备性能数据"}), 404

@app.route('/get_cpu_info', methods=['POST'])
def get_cpu_info():
    data = request.json
    sn = data.get('device_name')
    ids = data.get('other_field')

    cpu_info = db_operations.get_cpu_info(sn, ids)
    if cpu_info:
        return jsonify(cpu_info)
    else:
        return jsonify({"message": "未找到相关数据"}), 404

@app.route('/get_mem_info', methods=['POST'])
def get_mem_info():
    data = request.json
    sn = data.get('device_name')
    ids = data.get('other_field')

    mem_info = db_operations.get_mem_info(sn, ids)
    if mem_info:
        return jsonify(mem_info)
    else:
        return jsonify({"message": "未找到相关数据"}), 404

@app.route('/get_fps_info', methods=['POST'])
def get_fps_info():
    data = request.json
    sn = data.get('device_name')
    ids = data.get('other_field')

    fps_info = db_operations.get_fps_info(sn, ids)
    if fps_info:
        return jsonify(fps_info)
    else:
        return jsonify({"message": "未找到相关数据"}), 404

if __name__ == '__main__':
    #get_devices()
    #app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5100)