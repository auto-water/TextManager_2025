import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // 引入路由配置
import store from './store'   // 引入 Vuex store
import axios from 'axios'

// (可选) 如果使用 Element Plus
// import ElementPlus from 'element-plus'
// import 'element-plus/dist/index.css'

// 配置 Axios 默认 baseURL (根据你的后端API地址调整)
axios.defaults.baseURL = 'http://localhost:8000/api'; // Django 开发服务器地址

// Axios 请求拦截器，用于在每个请求中附加 Token
axios.interceptors.request.use(config => {
  const token = store.state.user.token; // 从 Vuex store 获取 token
  if (token) {
    config.headers.Authorization = `Token ${token}`; // DRF Token
    // 如果使用 JWT, 通常是 `Bearer ${token}`
  }
  return config;
}, error => {
  return Promise.reject(error);
});


const app = createApp(App)

app.use(router) // 使用路由
app.use(store)  // 使用 Vuex
// app.use(ElementPlus) // 如果使用 Element Plus

// 将 axios 挂载到全局属性，方便组件内通过 this.$axios 调用 (Options API)
// 或者在 Composition API 中直接导入使用
// app.config.globalProperties.$axios = axios; // 不太推荐，推荐在api层封装

app.mount('#app')