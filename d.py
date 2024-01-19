import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
def update_plot():
    start_time = start_var.get()
    # end_time = end_var.get()

    # data = pd.read_csv('/Users/yangcong/Downloads/mobileperf-master/results/com.yangcong345.android.phone/2023_12_28_11_31_53/cpuinfo.csv')
    filtered_data = data[(data['datetime'] >= start_time)]

    ax.clear()
    ax.plot(filtered_data['datetime'], filtered_data['device_cpu_rate%'])
    ax.set_xlabel('时间')
    ax.set_ylabel('设备CPU利用率 %')
    ax.set_title('设备CPU利用率')

    # 更新画布
    canvas.draw()

# 创建Tkinter窗口
root = tk.Tk()
root.title("时间范围选择")

# 添加开始时间选择框
start_label = ttk.Label(root, text="开始时间:")
start_label.pack()
start_var = tk.StringVar()
start_entry = ttk.Entry(root, textvariable=start_var)
start_entry.pack()

# # 添加结束时间选择框
# end_label = ttk.Label(root, text="结束时间:")
# end_label.pack()
# end_var = tk.StringVar()
# end_entry = ttk.Entry(root, textvariable=end_var)
# end_entry.pack()

# 开始持续刷新
def start_refresh():
    update_plot()  # 更新图表
    root.after(5000, start_refresh)  # 每5秒刷新一次
# 初始化数据
data = pd.read_csv('/Users/yangcong/PycharmProjects/Perf/R/_192.168.10.2:6666/results/com.yangcong345.android.phone/2023_12_28_19_42_55/cpuinfo.csv')
data['datetime'] = pd.to_datetime(data['datetime'], format='%Y-%m-%d %H-%M-%S')

# 创建图表
fig = Figure(figsize=(5, 4), dpi=100)
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()
# 添加按钮以更新绘图
update_button = ttk.Button(root, text="确认", command=update_plot)
update_button.pack()

# 初始化画布和子图
# fig, ax = plt.subplots()

root.mainloop()
