<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-brand">
        <router-link to="/" class="brand-text">
          <svg><!-- 可以放一个简单的SVG Logo -->
            <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
          </svg>
          文章管理器
        </router-link>
      </div>
      <div class="navbar-menu">
        <router-link to="/home" class="navbar-item">首页</router-link>
        <router-link v-if="isAuthenticated" to="/drafts" class="navbar-item">草稿箱</router-link>
        <router-link v-if="isAuthenticated" to="/editor" class="navbar-item ">写文章</router-link>
        <router-link to="/explore" class="navbar-item">探索</router-link>
      </div>
      <div class="navbar-end">
        <div v-if="isAuthenticated && currentUser" class="user-actions">
          <div class="user-greeting">你好, {{ currentUser.username }}</div>
          <!-- 可以添加下拉菜单放置管理员链接和登出 -->
          <router-link v-if="isAdmin" to="/categories" class="navbar-item admin-link">分类管理</router-link>
          <router-link v-if="isAdmin" to="/admin/users" class="navbar-item admin-link">用户管理</router-link>
          <button @click="handleLogout" class="button is-danger is-small">登出</button>
        </div>
        <div v-else class="auth-actions">
          <router-link to="/login" class="button is-light">登录</router-link>
          <router-link to="/register" class="button is-primary">注册</router-link>
        </div>
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
/* ...existing code... */

.navbar {
  background: linear-gradient(90deg, #e3f0ff 0%, #f8fafc 100%);
  border-radius: 0 0 22px 22px;
  box-shadow: 0 6px 24px rgba(21, 101, 192, 0.10);
  padding: 1.1rem 2.5rem 1.1rem 2.5rem;
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100%;
  transition: box-shadow 0.3s;
}

.navbar-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1280px;
  margin: 0 auto;
}

.navbar-brand .brand-text {
  display: flex;
  align-items: center;
  font-size: 2rem;
  font-weight: 800;
  color: #1976d2;
  letter-spacing: 2.5px;
  text-shadow: 0 2px 12px rgba(21,101,192,0.10);
  transition: color 0.2s;
}

.navbar-brand .brand-text:hover {
  color: #0d47a1;
}

.navbar-brand svg {
  width: 38px;
  height: 38px;
  margin-right: 12px;
  fill: #1976d2;
  filter: drop-shadow(0 2px 8px rgba(25,118,210,0.13));
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  position: relative;
}

.navbar-item {
  padding: 0.5rem 1.3rem;
  color: #495057;
  text-decoration: none;
  border-radius: 0.7rem;
  font-weight: 600;
  font-size: 1.08rem;
  position: relative;
  background: transparent;
  transition: background 0.22s, color 0.22s, transform 0.18s;
}

.navbar-item:not(:last-child)::after {
  content: '';
  display: inline-block;
  width: 2px;
  height: 20px;
  background: #e0e7ef;
  position: absolute;
  right: -0.7rem;
  top: 50%;
  transform: translateY(-50%);
  border-radius: 2px;
}

.navbar-item:hover,
.navbar-item.router-link-exact-active {
  background: #e3f2fd;
  color: #1976d2;
  transform: translateY(-2px) scale(1.07);
  box-shadow: 0 2px 12px rgba(25,118,210,0.09);
}

.user-greeting {
  color: #1976d2;
  font-weight: 700;
  margin-right: 0.7rem;
  font-size: 1.05rem;
}

.admin-link {
  font-size: 1rem;
  color: #6c757d;
  font-weight: 700;
  border: 1.5px solid #e3f2fd;
  border-radius: 0.5rem;
  padding: 0.35rem 1rem;
  margin-left: 0.7rem;
  background: #f5faff;
  transition: background 0.18s, color 0.18s, border 0.18s;
}
.admin-link:hover {
  color: #1976d2;
  background: #e3f2fd;
  border-color: #bbdefb;
}

.navbar-end .button.is-small {
  padding: 0.38rem 1rem;
  font-size: 1rem;
  border-radius: 0.5rem;
  margin-left: 0.5rem;
}

.auth-actions .button {
  margin-left: 0.5rem;
}

@media (max-width: 900px) {
  .navbar-container {
    flex-direction: column;
    align-items: stretch;
    padding: 0.5rem 0;
  }
  .navbar-menu {
    margin-top: 0.7rem;
    gap: 0.4rem;
    justify-content: flex-start;
  }
  .navbar-end {
    margin-top: 0.7rem;
    width: 100%;
    justify-content: flex-end;
  }
}
</style>