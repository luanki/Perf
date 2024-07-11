import { createRouter, createWebHistory } from 'vue-router';
import DeviceList from '../components/DeviceList.vue';
import DeviceDetails from '../components/DeviceDetails.vue';

const routes = [
  {
    path: '/',
    name: 'DeviceList',
    component: DeviceList
  },
  {
    path: '/DeviceDetails',
    name: 'DeviceDetails',
    component: DeviceDetails,
    props: true
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
