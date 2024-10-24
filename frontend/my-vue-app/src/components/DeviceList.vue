<template>
  <div class="page">
    <!-- Sidebar -->
    <aside class="navbar navbar-vertical navbar-expand-sm navbar-dark">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button">
          <span class="navbar-toggler-icon"></span>
        </button>
        <h1 class="navbar-brand navbar-brand-autodark">
          <a href="#">
            <img src="../assets/logo.png" width="110" height="32" alt="Tabler" class="navbar-brand-image">
          </a>
        </h1>
        <div class="collapse navbar-collapse" id="sidebar-menu">
          <ul class="navbar-nav pt-lg-3">
            <li class="nav-item">
              <a class="nav-link" href="./">
                <span class="nav-link-title">Home</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">
                <span class="nav-link-title">Link 1</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">
                <span class="nav-link-title">Link 2</span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">
                <span class="nav-link-title">Link 3</span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </aside>

    <div class="page-wrapper">
      <div class="page-header d-print-none">
        <div class="container-xl">
          <div class="row g-2 align-items-center">
            <div class="col">
              <h2 class="page-title">设备列表</h2>
            </div>
          </div>
        </div>
      </div>
      
      <div class="page-body">
        <div class="container-xl">
          <div class="row row-deck row-cards">
            <div class="table-responsive">
              <table class="table table-vcenter">
                <thead>
                  <tr>
                    <th>Id</th>
                    <th>设备ID</th>
                    <th>创建时间</th>
                    <th class="w-1"></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="device in devices" :key="device.device_id">
                    <td>{{ device.device_id }}</td>
                    <td class="text-secondary"><a href="#" class="text-reset">{{ device.device_name }}</a></td>
                    <td class="text-secondary">{{ device.created_at }}</td>
                    <td>
                      <router-link :to="{ path: '/DeviceDetails', query: { device_name: device.device_name, other_field: device.other_field } }" target="_blank">
                        View
                      </router-link>
                      <button @click="disconnectDevice(device.device_id, device.tcp_port)">Disconnect</button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { io } from 'socket.io-client';
import axios from 'axios';

export default {
  name: 'DeviceList',
  data() {
    return {
      devices: []
    };
  },
  created() {
    this.fetchDevices();
    this.setupSocket();
  },
  methods: {
    fetchDevices() {
      axios.get('http://127.0.0.1:5500/latest_ids')
        .then(response => {
          this.devices = response.data;
        })
        .catch(error => {
          console.error("Error fetching devices:", error);
        });
    },
    setupSocket() {
      const socket = io('http://127.0.0.1:5100'); // Replace with your Flask SocketIO server URL
      socket.on('new_device', (deviceInfo) => {
        this.devices.push(deviceInfo);
      });
    },
    disconnectDevice(deviceId, tcpPort) {
      axios.post('http://127.0.0.1:5100/api/disconnect', {
        deviceId: deviceId,
        tcpPort: tcpPort
      })
      .then(response => {
        console.log(response.data.message);
        // Optionally, refresh the device list
        this.fetchDevices();
      })
      .catch(error => {
        console.error("Error disconnecting device:", error);
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
