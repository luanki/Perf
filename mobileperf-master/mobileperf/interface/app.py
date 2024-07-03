from flask import Flask, jsonify
from flask_cors import CORS
from mobileperf.android.DB_utils import DatabaseOperations

app = Flask(__name__)
CORS(app)  # 添加CORS支持
db_operations = DatabaseOperations()

@app.route('/latest_ids', methods=['GET'])
def get_devices():
    devices = db_operations.get_all_devices()
    if devices:
        return jsonify(devices)
    else:
        return jsonify({"message": "未找到设备"})

if __name__ == '__main__':
    app.run(debug=True)
