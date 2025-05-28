<template>
  <div id="app-container">
    <Navbar />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
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
body {
  margin: 0;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #f4f6f8;
}

#app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto; /* 居中主要内容区域 */
  width: 100%;
  box-sizing: border-box;
}

/* 简单的页面过渡效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 可以添加更多全局样式 */
button {
  padding: 8px 15px;
  border: 1px solid #42b983;
  background-color: #42b983;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  margin: 5px;
}
button:hover {
  background-color: #3aa875;
}
button:disabled {
  background-color: #ccc;
  border-color: #ccc;
  cursor: not-allowed;
}

input[type="text"],
input[type="email"],
input[type="password"],
select,
textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 1em;
}
textarea {
  min-height: 150px;
  resize: vertical;
}

.error-message {
  color: red;
  margin-bottom: 10px;
  font-size: 0.9em;
}

.loading-indicator {
  text-align: center;
  padding: 20px;
  font-size: 1.2em;
}
</style>