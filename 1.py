import pandas as pd
import matplotlib.pyplot as plt
import glob
import csv

def read_csv_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        return pd.DataFrame(data)

# 获取第一个目录下的所有cpuinfo.csv文件
file_paths = glob.glob('/Users/yangcong/PycharmProjects/Perf/R/_192.168.10.77:9999/results/com.yangcong345.android.phone/*/cpuinfo.csv')
first_directory_files = file_paths[0]

latest_data = read_csv_data(first_directory_files)

# 转换datetime列的格式
latest_data['datetime'] = pd.to_datetime(latest_data['datetime'], format='%Y-%m-%d %H-%M-%S')

# 创建折线图
plt.figure(figsize=(10, 6))
plt.plot(latest_data['datetime'], latest_data['device_cpu_rate%'], label='Device CPU Rate')
plt.xlabel('Time')
plt.ylabel('CPU Rate (%)')
plt.title('Device CPU Rate Over Time')
plt.legend()
plt.show()
