import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
# data = pd.read_csv('/Users/yangcong/Downloads/mobileperf-master/results/com.yangcong345.android.phone/2023_11_15_14_39_48/cpuinfo.csv')
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize an empty plot
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)
ax.set_xlabel('Time')
ax.set_ylabel('Device CPU Rate %')
ax.set_title('Real-time Device CPU Rate')

def update(frame):
    # Read the updated CSV file
    data = pd.read_csv('/Users/yangcong/PycharmProjects/Perf/R/_192.168.10.2:6666/results/com.yangcong345.android.phone/2023_12_28_19_42_55/cpuinfo.csv')
    ax.clear()
    ax.plot(data['datetime'], data['device_cpu_rate%'], marker='o', linestyle='-')
    ax.set_xlabel('Time')
    ax.set_ylabel('Device CPU Rate %')
    ax.set_title('Real-time Device CPU Rate')
    plt.xticks(rotation=45)




