<template>
  <div>
    <h1>Data Visualization</h1>
    <div id="chart" style="width: 100%; height: 400px;"></div>
  </div>
</template>
<script>
import * as echarts from 'echarts';

export default {
  data() {
    return {
      chartData: null
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      fetch('http://127.0.0.1:5999/get_all_data')
        .then(response => response.json())
        .then(data => {
          this.chartData = data;
          if (this.chartData) {
            this.renderChart();  // 只有在数据存在时才执行渲染图表的操作
          }
        })
        .catch(error => console.error('Error:', error));
    },
    renderChart() {
      // 渲染图表之前先检查数据是否存在
      if (this.chartData) {
        const myChart = echarts.init(document.getElementById('chart'));

        // 数据处理
        const timeData = this.chartData.labels;
        const cpuRateData = this.chartData.values;

        myChart.setOption({
          title: {
            text: 'CPU Rate Over Time'
          },
          tooltip: {
            trigger: 'axis',
            formatter: '{b} <br/> CPU Rate: {c}%'
          },
          xAxis: {
            type: 'category',
            data: timeData
          },
          yAxis: {
            type: 'value'
          },
          series: [{
            data: cpuRateData,
            type: 'line',
            smooth: true
          }]
        });
      }
    }
  }
};
</script>