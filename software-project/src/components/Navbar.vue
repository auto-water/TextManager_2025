<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <router-link to="/" class="navbar-item brand-text">文章管理器</router-link>
    </div>
    <div class="navbar-menu">
      <router-link to="/home" class="navbar-item">首页</router-link>
      <router-link to="/explore" class="navbar-item">探索</router-link> <!-- 假设有个探索页 -->
      <router-link v-if="isAuthenticated" to="/drafts" class="navbar-item">草稿箱</router-link>
      <router-link v-if="isAuthenticated" to="/editor" class="navbar-item">写文章</router-link>
    </div>
    <div class="navbar-end">
      <div v-if="isAuthenticated && currentUser" class="navbar-item user-info">
        <span>你好, {{ currentUser.username }}</span>
        <img v-if="currentUser.avatar_url" :src="currentUser.avatar_url" alt="avatar" class="user-avatar"/>
        <div v-else class="user-avatar-placeholder">{{ currentUser.username.charAt(0).toUpperCase() }}</div>
        <router-link v-if="isAdmin" to="/categories" class="navbar-item admin-link">分类管理</router-link>
        <router-link v-if="isAdmin" to="/admin/users" class="navbar-item admin-link">用户管理</router-link>
        <button @click="handleLogout" class="navbar-item logout-button">登出</button>
      </div>
      <div v-else class="navbar-item">
        <router-link to="/login" class="button is-light">登录</router-link>
        <router-link to="/register" class="button is-primary">注册</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const isAuthenticated = computed(() => store.getters['user/isAuthenticated']);
const currentUser = computed(() => store.getters['user/currentUser']);
const isAdmin = computed(() => store.getters['user/isAdmin']);

const handleLogout = async () => {
  try {
    await store.dispatch('user/logoutUser');
    router.push('/login');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};
</script>

<style scoped>
.navbar {
  background-color: #fff;
  padding: 0.5rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.navbar-brand {
  display: flex;
  align-items: center;
}
.brand-text {
  font-size: 1.5em;
  font-weight: bold;
  color: #333;
}
.navbar-menu {
  display: flex;
  align-items: center;
}
.navbar-item {
  padding: 0.5rem 0.75rem;
  color: #555;
  text-decoration: none;
}
.navbar-item:hover, .navbar-item.router-link-active {
  color: #42b983; /* Vue green */
}
.navbar-end {
  display: flex;
  align-items: center;
}
.user-info {
  display: flex;
  align-items: center;
}
.user-info span {
  margin-right: 10px;
}
.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}
.user-avatar-placeholder {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #42b983;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 10px;
}
.logout-button, .button.is-light, .button.is-primary {
  margin-left: 0.5rem;
  padding: 0.5em 1em;
  border-radius: 4px;
  text-decoration: none;
  cursor: pointer;
}
.logout-button {
    background-color: #f14668;
    color: white;
    border: none;
}
.logout-button:hover {
    background-color: #ee3058;
}
.button.is-light {
    background-color: #f5f5f5;
    color: #363636;
    border: 1px solid #dbdbdb;
}
.button.is-primary {
    background-color: #42b983;
    color: white;
    border: none;
}
.admin-link {
    font-size: 0.9em;
    color: #ff3860; /* Or some other distinguishing color */
}
</style>