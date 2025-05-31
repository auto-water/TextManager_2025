// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // 引入路由配置
import store from './store'   // 引入 Vuex store
import axios from 'axios'

// 配置 Axios 默认 baseURL (根据你的后端API地址调整)
axios.defaults.baseURL = 'http://localhost:8000/api'; // Django 开发服务器地址

// Axios 请求拦截器，用于在每个请求中附加 Token
axios.interceptors.request.use(config => {
  const token = store.state.user.token; // 从 Vuex store 获取 token
  if (token) {
    // config.headers.Authorization = `Token ${token}`; // 这是 DRF Token 的格式
    config.headers.Authorization = `Bearer ${token}`; // 修改为 JWT (Bearer Token) 的格式
  }
  return config;
}, error => {
  return Promise.reject(error);
});


const app = createApp(App)

app.use(router)
app.use(store)

app.mount('#app')