import subprocess
import shutil
import os
import threading
from uiautomator import Device
import subprocess
import time
import psutil

import re

def sanitize_device_id(device_id):
    # Replace invalid characters with underscores
    sanitized_id = re.sub(r'[^\w\-_]', '_', device_id)
    return sanitized_id
def run_command_in_directory(command, directory):
    subprocess.run(f"cd {directory} && {command}", shell=True)

# def monitor_run_sh(device_id):
#     time.sleep(3)  # 每3秒检查一次
#     while True:
#         # 获取当前运行的进程列表
#         running_processes = [proc.name() for proc in psutil.process_iter(['pid', 'name', 'exe'])]
#
#         # 检查 run.sh 进程是否在列表中
#         run_sh_processes = [proc for proc in running_processes if 'run.sh' in proc]
#         if run_sh_processes:
#             print(f"run.sh 进程正在运行，设备ID: {device_id}")
#         else:
#             print(f"run.sh 进程停止运行，执行其他操作，设备ID: {device_id}")
#             # 在这里执行您想要的操作，比如执行另一个Python文件
#             subprocess.run(['python', 'Ear.py', device_id])
#             break
#         time.sleep(1)  # 每3秒检查一次



# 创建一个线程列表用于存储每个 sh 文件的执行线程
threads = []

# 执行 adb 命令以获取已连接设备列表
adb_process = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, _ = adb_process.communicate()

# 解析输出，提取设备列表和计算设备数量
device_lines = output.decode().split('\n')[1:-2]  # 提取设备列表
device_count = len(device_lines)
source_mobileperf_folder = r"C:\Users\yangcong\PycharmProjects\Perf\mobileperf-master"  # MobilePerf源文件夹路径
# 打印每个设备的 ID 并执行相应操作
for device_line in device_lines:

    if "device" in device_line:
        device_id = device_line.split('\t')[0]
        print(f"已连接设备 ID: {device_id}")

        # In the loop where you handle device IDs:
        target_device_id = device_id.replace(':', '_').replace('.', '_')
        target_mobileperf_folder = rf"C:\Users\yangcong\PycharmProjects\Perf\R\_{target_device_id}"  # 根据设备ID创建目标MobilePerf文件夹路径
        shutil.rmtree(target_mobileperf_folder, ignore_errors=True)  # 删除已存在的目标MobilePerf文件夹（如果存在的话）
        shutil.copytree(source_mobileperf_folder, target_mobileperf_folder)  # 复制源MobilePerf文件夹到目标MobilePerf文件夹
        print(f"MobilePerf文件夹 {source_mobileperf_folder} 已成功复制为 {target_mobileperf_folder}")  # 打印复制文件夹的信息
        config_file_path = os.path.join(target_mobileperf_folder, "config.conf")  # 配置文件路径
        # 打开配置文件，并进行相应的修改
        with open(config_file_path, 'r') as file:
            lines = file.readlines()
        with open(config_file_path, 'w') as file:
            for line in lines:
                if line.startswith("serialnum="):
                    file.write(f"serialnum={device_id}\n")

                elif line.startswith("monkey="):
                    file.write("# " + line)  # Comment out the original monkey command
                    file.write(
                        f"monkey=true\n")  # Write the modified monkey command
                else:
                    file.write(line)

        # 执行 mtklog start 命令，并将其发送到后台
        subprocess.run(["adb", "shell", "am", "start", "-n", "com.debug.loggerui/.MainActivity"])
        d = Device()
        time.sleep(2)  # 增加一些延迟等待界面加载完成
        # 点击指定元素
        d(resourceId='com.debug.loggerui:id/startStopToggleButton').click()
        time.sleep(2)  # 增加一些延迟等待界面加载完成
        # 将mtklog退到后台
        subprocess.run(['adb', '-s', device_id, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])

        # 执行 run.sh 文件（假设 run.sh 位于 MobilePerf 目录中）
        sh_directory = rf"C:\Users\yangcong\PycharmProjects\Perf\R\_{device_id}"
        sh_file = r"run.bat"
        # 进入 sh 文件所在目录
        #subprocess.run(f"cd {sh_directory} && sh {sh_file}", shell=True)
        # 创建并启动一个新的线程来执行命令
        thread = threading.Thread(target=run_command_in_directory, args=(sh_file, sh_directory))
        threads.append(thread)
        thread.start()
            #file.write(f"\nDevice ID: {device_id}\n")  # 在配置文件末尾添加设备ID信息

        # 执行 fps_run.py 文件，并将设备ID作为参数传递
        py_file = r"C:\Users\yangcong\PycharmProjects\Perf\mobileperf-master\mobileperf\android\fps_run.py"
        # 创建并启动一个新的线程来执行命令
        thread_py = threading.Thread(target=run_command_in_directory,
                                     args=(f"python {py_file} {device_id}", sh_directory))
        threads.append(thread_py)
        thread_py.start()

        # # 创建并启动一个线程来执行打开应用程序的命令
        # open_app_thread = threading.Thread(target=run_command_in_directory,
        #                                    args=(f"adb shell am start -n com.debug.loggerui/.MainActivity", ""))
        # d = Device()
        # time.sleep(2)  # 增加一些延迟等待界面加载完成
        # # 点击指定元素
        # d(resourceId='com.debug.loggerui:id/startStopToggleButton').click()
        # threads.append(open_app_thread)
        # open_app_thread.start()
        # subprocess.run(['adb', '-s', device_id, 'shell', 'input', 'keyevent', 'KEYCODE_HOME'])

# 等待所有线程执行完毕
for thread in threads:
    thread.join()