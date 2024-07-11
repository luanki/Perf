from flask import Flask, jsonify
from flask_cors import CORS
from mobileperf.android.DB_utils import DatabaseOperations
from datetime import datetime
app = Flask(__name__)
CORS(app)  # 添加CORS支持
db_operations = DatabaseOperations()

@app.route('/latest_ids', methods=['GET'])
def get_devices():
    devices = db_operations.get_all_devices()
    if devices:
        # 先对设备数据按创建时间排序，最新的排在最前面
        devices_sorted = sorted(devices, key=lambda x: x[3], reverse=True)
        # 转换数据格式为键值对
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

if __name__ == '__main__':
    app.run(debug=True)
