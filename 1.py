import os
import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts
import glob

def generate_html(csv_file, output_directory):
    try:
        #print(csv_file)
        df = pd.read_csv(csv_file)
        #print(df)
        # Convert 'datetime' column to pandas Timestamp objects
        df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H-%M-%S')

        # Create the line chart
        line = (
            Line()
            .add_xaxis([d.strftime('%Y-%m-%d %H:%M:%S') for d in df['datetime']])
            .add_yaxis("Device CPU Rate (%)", df['device_cpu_rate%'].tolist())
            .set_global_opts(
                title_opts=opts.TitleOpts(title="Device CPU Rate Over Time"),
                xaxis_opts=opts.AxisOpts(type_="time"),
                yaxis_opts=opts.AxisOpts(type_="value"),
                legend_opts=opts.LegendOpts(is_show=True),
                toolbox_opts=opts.ToolboxOpts(is_show=True),
                datazoom_opts=opts.DataZoomOpts(),
            )
        )

        # Save as HTML file
        output_file = os.path.join(output_directory, "1.html")
        line.render(output_file)

    except Exception as e:
        print(f"Error processing {csv_file}: {e}")

def visualize_csv_files():
    directory = "/Users/yangcong/PycharmProjects/Perf/R/_192.168.50.102:3333/results/com.yangcong345.android.phone/"
    pattern = f"{directory}*/cpuinfo.csv"

    csv_files = glob.glob(pattern)
    for csv_file in csv_files:
        generate_html(csv_file, os.path.dirname(csv_file))

if __name__ == "__main__":
    visualize_csv_files()
