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
                <span class="nav-link-title">
                  Home
                </span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">
                <span class="nav-link-title">
                  Link 1
                </span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">
                <span class="nav-link-title">
                  Link 2
                </span>
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">
                <span class="nav-link-title">
                  Link 3
                </span>
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
              <h2 class="page-title">
                设备列表
              </h2>
            </div>
          </div>
        </div>
      </div>
      <div class="page-body">
        <div class="container-xl">
          <div class="row row-deck row-cards">
            <div class="col-sm-6 col-lg-3">
              <div class="card">
                <div class="card-body" style="height: 10rem">
                  <div class="d-flex align-items-center">
                    <div class="subheader">Status monitoring</div>
                    <div class="ms-auto lh-1">
                      <div class="dropdown">
                        <a class="dropdown-toggle text-secondary" href="#" data-bs-toggle="dropdown"
                          aria-haspopup="true" aria-expanded="false">Current month</a>
                        <div class="dropdown-menu dropdown-menu-end">
                          <a class="dropdown-item active" href="#">Current month</a>
                          <a class="dropdown-item" href="#">Last month</a>
                          <a class="dropdown-item" href="#">Last 3 months</a>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="d-flex align-items-baseline">
                    <div class="h1 mb-3 me-2">99.5%</div>
                    <div class="me-auto">
                      <span class="text-green d-inline-flex align-items-center lh-1">
                        2%
                        <svg xmlns="http://www.w3.org/2000/svg" class="icon ms-1" width="24" height="24"
                          viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round"
                          stroke-linejoin="round">
                          <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                          <polyline points="3 17 9 11 13 15 21 7" />
                          <polyline points="14 7 21 7 21 14" />
                        </svg>
                      </span>
                    </div>
                  </div>
                  <div class="mt-2">
                    <div class="tracking">
                      <div class="tracking-block bg-success" data-bs-toggle="tooltip" data-bs-placement="top"
                        title="Operational"></div>
                      <div class="tracking-block bg-danger" data-bs-toggle="tooltip" data-bs-placement="top"
                        title="Downtime"></div>
                      <div class="tracking-block bg-success" data-bs-toggle="tooltip" data-bs-placement="top"
                        title="Operational"></div>
                      <div class="tracking-block bg-warning" data-bs-toggle="tooltip" data-bs-placement="top"
                        title="Big load"></div>
                      <div class="tracking-block" data-bs-toggle="tooltip" data-bs-placement="top" title="No data">
                      </div>
                      <div class="tracking-block" data-bs-toggle="tooltip" data-bs-placement="top" title="No data">
                      </div>
                      ...
                    </div>
                  </div>
                </div>
              </div>
            </div>
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
                    <td class="text-secondary">
                      {{ device.created_at }}
                    </td>
                    <td>
                      <!-- 使用 router-link -->
                      <router-link :to="{ path: '/DeviceDetails', query: { device_name: device.device_name, other_field: device.other_field } }"
                        target="_blank">
                        View
                      </router-link>
                      <!-- <a href="#" @click="viewDevicePerfInfo(device)">View</a> -->

                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- 其他卡片内容 -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
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
  },
  methods: {
    fetchDevices() {
      axios.get('http://127.0.0.1:5000/latest_ids')
        .then(response => {
          this.devices = response.data;
          // console.log(this.devices);

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
