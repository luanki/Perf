<!-- src/components/Devices.vue -->
<template>
  <div>
    <h1>设备列表</h1>
    <div v-if="devices.length">
      <ul>
        <li v-for="device in devices" :key="device.device_id">
          {{ device.device_name }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>未找到设备</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      devices: []
    };
  },
  created() {
    this.fetchDevices();
  },
  methods: {
    fetchDevices() {
      axios.get('http://localhost:5000/latest_ids')
        .then(response => {
          this.devices = response.data;
        })
        .catch(error => {
          console.error("Error fetching devices:", error);
        });
    }
  }
};
</script>

<style scoped>
h1 {
  color: #42b983;
}
</style>
