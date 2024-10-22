<template>
    <!-- <div>
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
    </div> -->
    <div class="card">
        <h2>CPU</h2>
        <div v-if="devicePerfInfo">
            <apexchart type="area" height="350" :options="cpuChartOptions" :series="cpuSeries"></apexchart>
        </div>
    </div>
    <div class="card">
        <h2>Memory</h2>
        <div v-if="deviceMemInfo">
            <apexchart type="area" height="350" :options="memChartOptions" :series="memSeries"></apexchart>
        </div>
    </div>
    <div class="card">
        <h2>FPS</h2>
        <div v-if="deviceFpsInfo">
            <apexchart type="area" height="350" :options="fpsChartOptions" :series="fpsSeries"></apexchart>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import VueApexCharts from 'vue3-apexcharts';

export default {
    name: 'DeviceDetails',
    components: {
        apexchart: VueApexCharts
    },
    data() {
        return {
            deviceData: null,
            devicePerfInfo: null,
            cpuChartOptions: {
                chart: {
                    type: 'area',
                    height: 350,
                    animations: {
                        enabled: true,
                        easing: 'linear',
                        dynamicAnimation: {
                            speed: 1000
                        }
                    },
                },
                xaxis: {
                    type: 'datetime',
                    labels: {
                        datetimeFormatter: {
                            year: 'yyyy',
                            month: "MMM 'yy",
                            day: 'dd MMM',
                            hour: 'HH:mm'
                        },
                        style: {
                            color: '#fff',
                        }

                    },
                    title: {
                        text: '时间',
                        style: {
                            color: '#fff'
                        }
                    }
                },
                tooltip: {
                    enabled: true,
                    x: {
                        format: 'HH:mm:ss'
                    }
                },
                title: {
                    text: 'CPU',
                    align: 'left'
                },
                stroke: {
                    width: 2
                },
                series: []
            },
            memChartOptions: {
                chart: {
                    type: 'area',
                    height: 350,
                    animations: {
                        enabled: true,
                        easing: 'linear',
                        dynamicAnimation: {
                            speed: 1000
                        }
                    },
                },
                xaxis: {
                    type: 'datetime',
                    labels: {
                        datetimeFormatter: {
                            year: 'yyyy',
                            month: "MMM 'yy",
                            day: 'dd MMM',
                            hour: 'HH:mm'
                        },
                        style: {
                            color: '#fff',
                        }
                    },
                    title: {
                        text: '时间',
                        style: {
                            color: '#fff'
                        }
                    }
                },
                tooltip: {
                    enabled: true,
                    x: {
                        format: 'HH:mm:ss'
                    }
                },
                title: {
                    text: 'Memory Usage',
                    align: 'left',
                    style: {
                        color: '#fff'
                    }
                },
                stroke: {
                    width: 2
                },
                series: []
            },
            fpsChartOptions: {
                chart: {
                    type: 'area',
                    height: 350,
                    animations: {
                        enabled: true,
                        easing: 'linear',
                        dynamicAnimation: {
                            speed: 1000
                        }
                    },
                },
                xaxis: {
                    type: 'datetime',
                    labels: {
                        datetimeFormatter: {
                            year: 'yyyy',
                            month: "MMM 'yy",
                            day: 'dd MMM',
                            hour: 'HH:mm'
                        },
                        style: {
                            color: '#fff',
                        }
                    },
                    title: {
                        text: '时间',
                        style: {
                            color: '#fff'
                        }
                    }
                },
                tooltip: {
                    enabled: true,
                    x: {
                        format: 'HH:mm:ss'
                    }
                },
                title: {
                    text: 'Fps',
                    align: 'left',
                    style: {
                        color: '#fff'
                    }
                },
                stroke: {
                    width: 2
                },
                series: []
            },
            cpuSeries: [],
            memSeries: [],
            fpsSeries: []
        };
    },
    created() {
        this.deviceData = {
            device_name: this.$route.query.device_name,
            other_field: this.$route.query.other_field
        };

        this.fetchDevicePerfInfo();
        this.fetchDeviceMemInfo();
        this.fetchDeviceFpsInfo();
    },
    methods: {
        fetchDevicePerfInfo() {
            const payload = {
                device_name: this.deviceData.device_name,
                other_field: this.deviceData.other_field
            };

            axios.post('http://127.0.0.1:5500/get_cpu_info', payload)
                .then(response => {
                    //console.log("API response:", response.data); 
                    this.devicePerfInfo = response.data;
                    this.processChartData();
                    // console.log(this.devicePerfInfo)
                })
                .catch(error => {
                    console.error("获取设备cpu信息出错:", error);
                });
        },
        fetchDeviceMemInfo() {
            const payload = {
                device_name: this.deviceData.device_name,
                other_field: this.deviceData.other_field
            };

            axios.post('http://127.0.0.1:5500/get_mem_info', payload)
                .then(response => {
                    this.deviceMemInfo = response.data;
                    this.processMemChartData();
                })
                .catch(error => {
                    console.error("获取设备memory信息出错:", error);
                });
        },
        fetchDeviceFpsInfo() {
            const payload = {
                device_name: this.deviceData.device_name,
                other_field: this.deviceData.other_field
            };

            axios.post('http://127.0.0.1:5500/get_fps_info', payload)
                .then(response => {
                    this.deviceFpsInfo = response.data;
                    this.processFpsChartData(); // 添加这行调用
                })
                .catch(error => {
                    console.error("获取设备fps信息出错:", error);
                });
        },
        processChartData() {

            const cpuSeries = this.devicePerfInfo.map(data => ({
                x: new Date(data.recorded_at + ' UTC').getTime(), // 加上 ' UTC' 以确保时间戳被解释为UTC时间
                y: data.device_cpu_rate
            }));

            const pidCpuSeries = this.devicePerfInfo.map(data => ({
                x: new Date(data.recorded_at + ' UTC').getTime(),
                y: data.pid_cpu_rate
            }));

            const userRateSeries = this.devicePerfInfo.map(data => ({
                x: new Date(data.recorded_at + ' UTC').getTime(),
                y: data.user_rate
            }));


            this.cpuSeries = [
                {
                    name: 'CPU Rate',
                    data: cpuSeries
                },
                {
                    name: 'PID CPU Rate',
                    data: pidCpuSeries
                },
                {
                    name: 'User Rate',
                    data: userRateSeries
                }
            ];
        },
        processMemChartData() {
            const memSeries = this.deviceMemInfo.map(data => ({
                x: new Date(data.recorded_at + ' UTC').getTime(),
                y: data.total_ram
            }));

            const pidMemSeries = this.deviceMemInfo.map(data => ({
                x: new Date(data.recorded_at + ' UTC').getTime(),
                y: data.pid_pss
            }));

            this.memSeries = [
                {
                    name: 'Memory Totel',
                    data: memSeries
                },
                {
                    name: 'Memory Pid Pss',
                    data: pidMemSeries
                },
            ];
        },
        processFpsChartData() {
            const fpsSeries = this.deviceFpsInfo.map(data => ({
                x: new Date(data.recorded_at + ' UTC').getTime(),
                y: data.fps
            }));

            const jankSeries = this.deviceFpsInfo.map(data => ({
                x: new Date(data.recorded_at + ' UTC').getTime(),
                y: data.jank
            }));

            this.fpsSeries = [
                {
                    name: 'Fps',
                    data: fpsSeries
                },
                {
                    name: 'Jank',
                    data: jankSeries
                },
            ];
        }
    }
};
</script>

<style scoped>
h1 {
    color: #42b983;
}
</style>
