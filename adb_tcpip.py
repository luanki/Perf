import subprocess
import random
import re
import threading
import time

connected_devices = {}  # 用于存储已连接的设备，格式为 {device_id: (device_ip, tcp_port)}
monitored_devices = set()  # 用于存储已监控的设备
monitoring_active = True  # 标志变量，用于控制监控循环

def adb_shell_command(device_id, command):
    """执行 adb shell 命令并返回输出"""
    cmd = f'adb -s {device_id} shell {command}'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"执行命令时发生错误: {result.stderr.strip()}")
    return result.stdout.strip()

def get_device_ip(device_id):
    """获取设备的 IP 地址"""
    ip_output = adb_shell_command(device_id, 'ip route')
    ip_match = re.search(r'src (\d+\.\d+\.\d+\.\d+)', ip_output)
    if not ip_match:
        raise Exception("无法找到设备的 IP 地址")
    return ip_match.group(1)

def get_random_port(used_ports):
    """生成一个随机端口，避免使用已占用的端口"""
    port = random.randint(1024, 65535)
    while port in used_ports:
        port = random.randint(1024, 65535)
    return port

def adb_tcpip_connect(device_id):
    """将设备切换到 TCP/IP 模式并连接"""
    global connected_devices, monitored_devices  # 引用全局变量

    # 获取设备的 IP 地址
    device_ip = get_device_ip(device_id)

    # 检查当前设备连接状态
    current_connection = connected_devices.get(device_id)
    if current_connection and current_connection[0] == device_ip:
        print(f"{device_id} 已连接，跳过连接操作。")
        return  # 已连接，跳过

    try:
        print(f"设备 IP: {device_ip}")

        # 获取已使用的端口（可选，手动定义，避免冲突）
        used_ports = {port for _, port in connected_devices.values()}  # 使用已连接设备的端口

        # 生成随机端口号
        tcp_port = get_random_port(used_ports)
        print(f"绑定端口: {tcp_port}")

        # 切换到 TCP/IP 模式（在本地执行）
        tcpip_command = f'adb -s {device_id} tcpip {tcp_port}'
        tcpip_result = subprocess.run(tcpip_command, shell=True, capture_output=True, text=True)
        if tcpip_result.returncode != 0:
            raise Exception(f"切换到 TCP/IP 模式失败: {tcpip_result.stderr.strip()}")

        print(f"{device_id} 已切换到 TCP/IP 模式，端口: {tcp_port}")

        # 连接到设备
        connect_command = f'adb connect {device_ip}:{tcp_port}'
        connect_result = subprocess.run(connect_command, shell=True, capture_output=True, text=True)
        if connect_result.returncode != 0:
            raise Exception(f"连接设备失败: {connect_result.stderr.strip()}")

        print(f"成功连接到设备 {device_ip}:{tcp_port}")
        # 更新已连接设备
        connected_devices[device_id] = (device_ip, tcp_port)  # 存储设备的 IP 和端口
        monitored_devices.add(device_id)  # 添加到监控列表

        # 等待一段时间以确保连接生效
        time.sleep(2)

        # 检查设备是否已成功连接
        check_command = 'adb devices'
        check_result = subprocess.run(check_command, shell=True, capture_output=True, text=True)
        print("当前连接状态:")
        print(check_result.stdout)

        # 检查是否成功连接
        if f'{device_ip}:{tcp_port}\tdevice' in check_result.stdout:
            print(f"{device_id} 连接成功。")

    except Exception as e:
        print(f"发生错误: {e}")

def monitor_devices():
    """监控设备连接状态"""
    while True:
        # 获取已连接设备列表
        result = subprocess.run('adb devices', shell=True, capture_output=True, text=True)
        lines = result.stdout.splitlines()[1:]  # 跳过第一行

        for line in lines:
            if line.strip() and 'device' in line:
                device_id = line.split('\t')[0]
                if device_id not in monitored_devices:
                    print(f"检测到设备: {device_id}")
                    adb_tcpip_connect(device_id)

        time.sleep(5)  # 每 5 秒检查一次

if __name__ == "__main__":
    # 启动设备监控线程
    monitor_thread = threading.Thread(target=monitor_devices, daemon=True)
    monitor_thread.start()

    # 主线程可以进行其他操作，或者保持运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("停止监控")
