import subprocess
import shutil
import os
import threading
from uiautomator import Device
import time
import psutil
import re
import platform
from flask import Flask, request, jsonify
app = Flask(__name__)
# 用于存储设备信息的字典
connected_devices = {}
device_threads = {}
device_processes = {}
# 新增一个字典来保存设备与startup进程的映射
startup_processes = {}

import sys
# 获取当前文件所在目录的绝对路径
base_dir = os.path.dirname(os.path.abspath(__file__))

# 获取 mobileperf-master 目录的路径
mobileperf_dir = os.path.join(base_dir, 'mobileperf-master')

# 添加 mobileperf-master 目录到 sys.path
sys.path.append(mobileperf_dir)

# 导入 DB_utils.py 中的某个函数
from mobileperf.android.DB_utils import DatabaseOperations


# 检测操作系统类型
is_windows = os.name == 'nt'
is_mac = platform.system() == 'Darwin'

# 创建一个线程列表用于存储每个sh文件的执行线程
threads = []

#执行adb命令以获取已连接设备列表
# adb_process = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# output, _ = adb_process.communicate()

#解析输出，提取设备列表和计算设备数量
# device_lines = output.decode().split('\n')[1:-2]  # 提取设备列表
# device_count = len(device_lines)

# 动态获取基路径（假设脚本位于项目的根目录）
base_path = os.path.dirname(os.path.abspath(__file__))

source_mobileperf_folder = os.path.join(base_path, "mobileperf-master")  # 源MobilePerf文件夹路径

# 获取所有当前的 startup 进程
def get_startup_processes():
    """获取当前运行的 startup 进程"""
    startup_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'python3' and 'startup.py' in proc.info['cmdline']:
            startup_processes.append(proc)
    return startup_processes

def sanitize_device_id(device_id):
    # 将无效字符替换为下划线
    sanitized_id = re.sub(r'[^\w\-_]', '_', device_id)
    return sanitized_id


device_threads = {}
stop_events = {}  # 存储设备线程的停止事件
def run_command_in_directory(command, directory):
    subprocess.run(command, cwd=directory, shell=True)





def handle_device_setup(device_id, tcp_port):
    """连接成功后执行设备的设置和性能测试"""
    target_device_id = device_id
    #target_device_id = f"host.docker.internal:{tcp_port}"  # 使用完整的设备 ID
    #print(target_device_id)

    # 如果设备线程已存在且在运行，先停止旧线程
    if target_device_id in device_threads and device_threads[target_device_id].is_alive():
        print(f"正在停止设备 {target_device_id} 的旧线程")
        stop_events[target_device_id].set()  # 设置停止事件
        device_threads[target_device_id].join()  # 等待线程停止


    base_path = os.path.dirname(os.path.abspath(__file__))
    source_mobileperf_folder = os.path.join(base_path, "mobileperf-master")

    # 创建目标 MobilePerf 文件夹路径
    target_mobileperf_folder = os.path.join(base_path, "R", f"_{sanitize_device_id(target_device_id)}")
    shutil.rmtree(target_mobileperf_folder, ignore_errors=True)  # 删除已存在的目标文件夹
    shutil.copytree(source_mobileperf_folder, target_mobileperf_folder)  # 复制源文件夹到目标文件夹
    print(f"MobilePerf文件夹 {source_mobileperf_folder} 已成功复制为 {target_mobileperf_folder}")

    # 修改配置文件
    config_file_path = os.path.join(target_mobileperf_folder, "config.conf")
    with open(config_file_path, 'r') as file:
        lines = file.readlines()
    with open(config_file_path, 'w') as file:
        for line in lines:
            if line.startswith("serialnum="):
                file.write(f"serialnum={target_device_id}\n")
            elif line.startswith("monkey="):
                file.write("# " + line)  # 注释掉原来的monkey命令
                file.write("monkey=true\n")  # 写入修改后的monkey命令
            else:
                file.write(line)

    sh_directory = os.path.join(base_path, "R", f"_{sanitize_device_id(target_device_id)}")
    if is_windows:
        sh_file = "run.bat"
        command = sh_file
    else:
        sh_file = "run.sh"
        command = f"sh {sh_file} {tcp_port}"

    # 创建一个新的停止事件
    # stop_event = threading.Event()
    # stop_events[target_device_id] = stop_event

    # 创建并启动一个新的线程来执行命令
    thread = threading.Thread(target=run_command_in_directory, args=(command, sh_directory))
    #threads.append(thread)
    device_threads[target_device_id] = thread
    thread.start()

    # time.sleep(2)  # 等待一段时间，以便进程启动
    # for proc in psutil.process_iter(['pid', 'name']):
    #     if proc.info['name'] == 'startup' and target_device_id not in startup_processes:
    #         print(f"记录设备 {target_device_id} 的 startup 进程: {proc.info['pid']}")
    #         startup_processes[target_device_id] = proc  # 绑定设备和进程
    #         break  # 找到后退出循环

    # 向数据库插入设备基本信息
    db_operations = DatabaseOperations()
    device_name = "未知"
    if device_id.startswith("S30"):
        device_name = "S30"
    elif device_id.startswith("Q20"):
        device_name = "Q20"

    try:
        db_operations.devices_info_insert(target_device_id, device_name)
    except Exception as db_e:
        print(db_e)
        print("devices_info插入数据库失败！！")


    # 执行 fps_run.py 文件，并将设备 ID 作为参数传递
    py_file = os.path.join(base_path, "mobileperf-master", "mobileperf", "android", "fps_run.py")
    py_file = py_file.replace('\r', '')  # 移除路径中的回车符
    # 创建并启动一个新的线程来执行命令
    thread_py = threading.Thread(target=run_command_in_directory, args=(f"python {py_file} {device_id}", sh_directory))
    #thread_py = threading.Thread(target=run_command_in_directory, args=(f"python {py_file} {target_device_id}", sh_directory))
    threads.append(thread_py)
    thread_py.start()

    # 记录线程
    # device_threads[target_device_id] = thread

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5200)