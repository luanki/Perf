
import logging
import time

from flask import Flask, request, jsonify
import subprocess
from flask_socketio import SocketIO, emit

app = Flask(__name__)
#socketio = SocketIO(app)

import devices_action
connected_devices = {}
#执行 adb devices 并返回设备列表
def get_connected_devices():
    adb_process = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = adb_process.communicate()
    device_lines = output.decode().split('\n')[1:-1]  # 提取设备列表
    devices = {}
    for line in device_lines:
        if '\tdevice' in line:
            device_id = line.split('\t')[0]
            devices[device_id] = f"host.docker.internal:{connected_devices.get(device_id)}"
    print(devices)
    return devices
@app.route('/api/report', methods=['POST'])
def report_device():
    """报告设备信息并尝试连接"""
    data = request.json
    device_id = data.get('deviceId')
    tcp_port = data.get('tcpPort')

    if device_id and tcp_port:
        print(f"接收到设备: {device_id}，端口: {tcp_port}")

        if device_id in connected_devices:
            return jsonify({"message": "设备已连接"}), 200

        connected_devices[device_id] = tcp_port

        # 尝试进行 adb 连接
        try:
            connect_command = f'adb connect host.docker.internal:{tcp_port}'
            result = subprocess.run(connect_command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"成功连接设备 {device_id}，端口: {tcp_port}")
                time.sleep(2)
                try:
                    devices_action.handle_device_setup(device_id, tcp_port)
                except Exception as e:
                    print(f"Error in handle_device_setup: {e}")
                #socketio.emit('new_device', {'device_id': device_id, 'tcp_port': tcp_port}, broadcast=True)
                return jsonify({"message": "设备信息已成功接收，已连接"}), 200
            else:
                print(f"连接设备 {device_id} 失败: {result.stderr}")
                return jsonify({"message": f"连接失败: {result.stderr}"}), 500

        except Exception as e:
            print(f"执行 adb connect 时发生错误: {e}")
            return jsonify({"message": f"发生错误: {str(e)}"}), 500

    return jsonify({"message": "无效请求"}), 400
@app.route('/api/disconnect', methods=['POST'])
def disconnect_device():
    data = request.json
    device_id = data.get('deviceId')
    tcp_port = data.get('tcpPort')

    if device_id in connected_devices:
        del connected_devices[device_id]
        logging.info(f"设备 {device_id} 断开连接，端口: {tcp_port}")

        # 执行 ADB 命令断开设备连接
        try:
            disconnect_command = f'adb disconnect host.docker.internal:{tcp_port}'
            result = subprocess.run(disconnect_command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"成功断开设备 {device_id} 的连接")
                return jsonify({"message": "设备已成功断开连接"}), 200
            else:
                logging.error(f"断开设备 {device_id} 失败: {result.stderr}")
                return jsonify({"message": "断开连接失败"}), 500
        except Exception as e:
            logging.error(f"断开连接时发生错误: {e}")
            return jsonify({"message": "断开连接失败"}), 500
    return jsonify({"message": "设备未连接"}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)

