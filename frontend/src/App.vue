<template>
  <div id="app-container">
    <Navbar />
    <div class="content-container">
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
import { onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

// 应用加载时，尝试获取当前用户信息（如果token存在）
onMounted(() => {
  if (store.getters['user/isAuthenticated']) {
    store.dispatch('user/fetchCurrentUser');
  }
});
</script>

<style>
/* 全局样式，或者在 assets/css/main.css 中引入 */
/* frontend/src/App.vue <style> (全局部分) */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"; /* 更现代的字体栈 */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #343a40; /* 深灰色，比纯黑更柔和 */
  background-color: #f8f9fa; /* 更亮的背景色 */
  line-height: 1.6; /* 改善可读性 */
}

#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content-container {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 24px; /* 稍微增加内边距 */
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.main-content {
  width: 100%;
  box-sizing: border-box;
}

/* 页面过渡效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease-out; /* 更快的过渡 */
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 统一按钮基础样式 (可以在这里定义，也可以在组件中覆盖) */
button, .button { /* 也为 <router-link class="button"> 服务 */
  display: inline-block; /* 确保 <router-link class="button"> 行为像按钮 */
  padding: 0.5rem 1rem; /* 使用 rem 单位 */
  font-size: 0.95rem;
  font-weight: 500;
  line-height: 1.5;
  text-align: center;
  text-decoration: none;
  vertical-align: middle;
  cursor: pointer;
  user-select: none;
  background-color: transparent;
  border: 1px solid transparent;
  border-radius: 0.3rem; /* 更圆润的边角 */
  transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  margin: 0.25rem; /* 统一外边距 */
}

/* 主要按钮样式 (例如: 搜索按钮, 注册按钮) */
.button.is-primary, button[type="submit"], .search-button {
  color: #fff;
  background-color: #007bff; /* 主题蓝色 */
  border-color: #007bff;
}
.button.is-primary:hover, button[type="submit"]:hover, .search-button:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

/* 次要/浅色按钮 (例如: 登录按钮) */
.button.is-light {
  color: #212529;
  background-color: #e9ecef; /* 浅灰色 */
  border-color: #dee2e6;
}
.button.is-light:hover {
  background-color: #dae0e5;
  border-color: #d3d9df;
}

/* 危险操作按钮 (例如: 登出, 删除) */
.button.is-danger, .logout-button, .delete-article-btn-list, .delete-btn-card {
  color: #fff;
  background-color: #dc3545; /* 主题红色 */
  border-color: #dc3545;
}
.button.is-danger:hover, .logout-button:hover, .delete-article-btn-list:hover, .delete-btn-card:hover {
  background-color: #c82333;
  border-color: #bd2130;
}


button:disabled, .button:disabled {
  background-color: #adb5bd; /* 禁用状态颜色 */
  border-color: #adb5bd;
  color: #6c757d;
  cursor: not-allowed;
  opacity: 0.65;
}

/* 表单元素基础样式 */
input[type="text"],
input[type="search"], /* 为搜索框添加 */
input[type="email"],
input[type="password"],
select,
textarea {
  display: block; /* 确保 select 也占满宽度 */
  width: 100%;
  padding: 0.5rem 0.75rem; /* 使用 rem */
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #495057;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
  margin-bottom: 1rem; /* 统一表单项间距 */
  box-sizing: border-box;
}

input[type="search"] { /* 特定于搜索框的样式 */
  -webkit-appearance: none; /* 移除默认的搜索框样式 (如 macOS 上的圆角和放大镜) */
}


input:focus, select:focus, textarea:focus {
  border-color: #80bdff;
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

textarea {
  min-height: 120px; /* 调整高度 */
  resize: vertical;
}

.error-message {
  color: #dc3545; /* 使用主题红色 */
  background-color: #f8d7da; /* 淡红色背景 */
  border: 1px solid #f5c6cb;
  padding: 0.75rem 1.25rem;
  margin-bottom: 1rem;
  border-radius: 0.25rem;
  font-size: 0.9em;
}

.loading-indicator {
  text-align: center;
  padding: 2rem;
  font-size: 1.2rem;
  color: #6c757d; /* 中性灰色 */
}
</style>