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
            <!-- <img src="..." width="110" height="32" alt="Tabler" class="navbar-brand-image"> -->
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
                <div class="card-body" style="height: 10rem"></div>
              </div>
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
