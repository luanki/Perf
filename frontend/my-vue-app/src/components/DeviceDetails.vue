<template>
    <div>
        <h1>设备详情</h1>
        <p v-if="deviceData">
            <strong>设备名称：</strong> {{ deviceData.device_name }}
        </p>
        <p v-if="deviceData">
            <strong>其他字段：</strong> {{ deviceData.other_field }}
        </p>
        <p v-else>
            加载中...
        </p>
        <div v-if="devicePerfInfo">
            <h2>API 响应</h2>
            <pre>{{ devicePerfInfo }}</pre>
        </div>
    </div>
    <div class="card">
        <div class="card-body">
            <div id="chart-social-referrals" class="chart-lg"></div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'DeviceDetails',
    data() {
        return {
            deviceData: null,
            devic: null
        };
    },
    created() {
        this.deviceData = {
            device_name: this.$route.query.device_name,
            other_field: this.$route.query.other_field
        };

        this.fetchDevicePerfInfo();
    },
    methods: {
        fetchDevicePerfInfo() {
            const payload = {
                device_name: this.deviceData.device_name,
                other_field: this.deviceData.other_field
            };

            axios.post('http://127.0.0.1:5000/view_device_perf_info', payload)
                .then(response => {
                    this.devicePerfInfo = response.data;
                    this.renderChart(); // 数据获取后调用方法渲染图表
                })
                .catch(error => {
                    console.error("获取设备性能信息出错:", error);
                });
        },
        renderChart() {
            if (this.devicePerfInfo) {
                const seriesData = [
                    {
                        name: "Facebook",
                        data: this.generateSeriesData(this.devicePerfInfo, 'facebook')
                    },
                    {
                        name: "Twitter",
                        data: this.generateSeriesData(this.devicePerfInfo, 'twitter')
                    },
                    {
                        name: "Dribbble",
                        data: this.generateSeriesData(this.devicePerfInfo, 'dribbble')
                    }
                ];

                window.ApexCharts && new ApexCharts(document.getElementById('chart-social-referrals'), {
                    chart: {
                        type: "line",
                        fontFamily: 'inherit',
                        height: 240,
                        parentHeightOffset: 0,
                        toolbar: {
                            show: false,
                        },
                        animations: {
                            enabled: false
                        },
                    },
                    fill: {
                        opacity: 1,
                    },
                    stroke: {
                        width: 2,
                        lineCap: "round",
                        curve: "smooth",
                    },
                    series: seriesData,
                    tooltip: {
                        theme: 'dark'
                    },
                    grid: {
                        padding: {
                            top: -20,
                            right: 0,
                            left: -4,
                            bottom: -4
                        },
                        strokeDashArray: 4,
                        xaxis: {
                            lines: {
                                show: true
                            }
                        },
                    },
                    xaxis: {
                        labels: {
                            padding: 0,
                        },
                        tooltip: {
                            enabled: false
                        },
                        type: 'datetime',
                        categories: this.devicePerfInfo.labels // 假设标签在 devicePerfInfo 中
                    },
                    yaxis: {
                        labels: {
                            padding: 4
                        },
                    },
                    colors: [tabler.getColor("facebook"), tabler.getColor("twitter"), tabler.getColor("dribbble")],
                    legend: {
                        show: true,
                        position: 'bottom',
                        offsetY: 12,
                        markers: {
                            width: 10,
                            height: 10,
                            radius: 100,
                        },
                        itemMargin: {
                            horizontal: 8,
                            vertical: 8
                        },
                    },
                }).render();
            }
        },
        generateSeriesData(devicePerfInfo, seriesName) {
            const seriesData = [];
            devicePerfInfo.forEach(dataPoint => {
                // 根据实际的 API 响应结构进行调整
                if (dataPoint.name === seriesName) {
                    seriesData.push(dataPoint.value); // 替换为包含系列数据的实际字段
                }
            });
            return seriesData;
        }
    }
};
</script>

<style scoped>
h1 {
    color: #42b983;
}
</style>

