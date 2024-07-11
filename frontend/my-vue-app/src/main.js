// import { createApp } from 'vue'
// import App from './App.vue'
// import router from './router'
 
// const app = createApp(App)
// app.use(router)
// app.mount('#app')
import { createApp } from 'vue';
import App from './App.vue';
import router from './router/index';  // 确保路径正确

createApp(App)
  .use(router)
  .mount('#app');
