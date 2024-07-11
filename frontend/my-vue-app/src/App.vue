<!-- src/App.vue -->
<!-- <template>
  <div id="app">
    <DeviceList />
  </div>
</template>

<script>
import DeviceList from './components/DeviceList.vue'; // 导入修正后的组件名称
import router from './router';

export default {
  name: 'App',
  components: {
    DeviceList // 注册修正后的组件名称
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style> -->
<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
