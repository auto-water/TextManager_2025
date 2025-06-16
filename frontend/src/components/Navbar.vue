<template>
  <nav class="navbar">
    <div class="navbar-container">
      <!-- 将导航栏分为左、中、右三部分，不再使用之前的两部分布局 -->
      <div class="navbar-brand">
        <router-link to="/" class="brand-text">
          <span class="brand-logo-wrapper">
            <svg class="brand-logo" viewBox="0 0 24 24">
              <defs>
                <linearGradient id="logo-gradient" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stop-color="#1976d2"/>
                  <stop offset="100%" stop-color="#42b983"/>
                </linearGradient>
              </defs>
              <!-- 新的文档/书本图标替代房子图标 -->
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z" fill="url(#logo-gradient)"/>
            </svg>
          </span>
          <span class="brand-title">文章管理器</span>
        </router-link>
      </div>
      
      <div class="navbar-menu">
        <router-link to="/home" class="navbar-item">首页</router-link>
        <router-link v-if="isAuthenticated" to="/drafts" class="navbar-item">草稿箱</router-link>
        <router-link v-if="isAuthenticated" to="/editor" class="navbar-item">写文章</router-link>
        <router-link to="/explore" class="navbar-item">探索</router-link>
      </div>
      
      <div class="navbar-end">
        <div v-if="isAuthenticated && currentUser" class="user-actions">
          <div class="user-info">
            <span class="user-greeting">你好, {{ currentUser.username }}</span>
            <div class="admin-links" v-if="isAdmin">
              <router-link to="/categories" class="admin-link">分类管理</router-link>
              <router-link to="/admin/users" class="admin-link">用户管理</router-link>
            </div>
            <button @click="handleLogout" class="button is-danger is-small">登出</button>
          </div>
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
.navbar {
  background: linear-gradient(90deg, #f0f7ff 0%, #fbfcfe 100%);
  border-radius: 0 0 25px 25px;
  box-shadow: 0 4px 20px rgba(21, 101, 192, 0.08);
  padding: 0.9rem 2rem;
  position: sticky;
  top: 0;
  z-index: 1000;
  width: 100vw; /* 修改为视口宽度 */
  margin-left: calc(-50vw + 50%); /* 使导航栏水平居中并覆盖整行 */
  transition: all 0.3s ease;
  box-sizing: border-box;
  overflow-x: hidden;
  left: 0;
  right: 0;
}

.navbar-container {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  align-items: center;
  max-width: 1280px;
  margin: 0 auto;
  width: 100%;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.navbar-brand .brand-text {
  display: flex;
  align-items: center;
  font-size: 1.8rem;
  font-weight: 800;
  color: #1976d2;
  letter-spacing: 1.5px;
  text-shadow: 0 2px 10px rgba(21,101,192,0.08);
  padding: 0.3rem 0.8rem 0.3rem 0.3rem;
  border-radius: 1.2rem;
  text-decoration: none;
  white-space: nowrap;
  transition: transform 0.3s ease;
}

/* 添加禁用悬停效果的规则 */
.navbar-brand .brand-text:hover {
  color: #1976d2;
  transform: none;
  box-shadow: none;
  background: transparent;
}

.brand-logo-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #e3f0ff 60%, #c8e6c9 100%);
  border-radius: 50%;
  width: 44px;
  height: 44px;
  margin-right: 12px;
  box-shadow: 0 3px 12px rgba(25,118,210,0.12);
  flex-shrink: 0;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.navbar-brand:hover .brand-logo-wrapper {
  transform: scale(1.05) rotate(5deg);
  box-shadow: 0 4px 15px rgba(25,118,210,0.18);
}

.brand-logo {
  width: 30px;
  height: 30px;
  display: block;
}

.brand-title {
  font-size: 1.8rem;
  font-weight: 800;
  background: linear-gradient(90deg, #1976d2 20%, #42b983 80%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.navbar-brand svg {
  width: 32px;
  height: 32px;
  margin-right: 10px;
  fill: #1976d2;
  filter: drop-shadow(0 2px 8px rgba(25,118,210,0.13));
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: flex-start;
  padding-left: 1.5rem;
  flex-wrap: wrap;
}

.navbar-item {
  padding: 0.6rem 1.1rem;
  color: #4a5568;
  text-decoration: none;
  border-radius: 0.8rem;
  font-weight: 600;
  font-size: 1.05rem;
  position: relative;
  background: transparent;
  transition: all 0.25s ease;
  white-space: nowrap;
}

.navbar-item:not(:last-child)::after {
  content: '';
  display: inline-block;
  width: 2px;
  height: 20px;
  background: #e0e7ef;
  position: absolute;
  right: -0.5rem;
  top: 50%;
  transform: translateY(-50%);
  border-radius: 2px;
  opacity: 0.7;
}

.navbar-item:hover {
  background: #e3f2fd;
  color: #1976d2;
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(25,118,210,0.12);
}

.navbar-item.router-link-exact-active {
  background: #e3f2fd;
  color: #1976d2;
  font-weight: 700;
  box-shadow: 0 4px 14px rgba(25,118,210,0.12);
}

.navbar-end {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.user-actions {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.9rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.user-greeting {
  color: #1976d2;
  font-weight: 700;
  font-size: 1.05rem;
  white-space: nowrap;
  background-color: #f0f7ff;
  padding: 0.4rem 0.8rem;
  border-radius: 0.6rem;
  box-shadow: 0 2px 8px rgba(25,118,210,0.08);
}

.admin-links {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.admin-link {
  font-size: 0.9rem;
  color: #5a6888;
  font-weight: 600;
  border: 1px solid #e3f2fd;
  border-radius: 0.6rem;
  padding: 0.35rem 0.7rem;
  background: #f5faff;
  transition: all 0.2s ease;
  text-decoration: none;
  white-space: nowrap;
}

.admin-link:hover {
  color: #1976d2;
  background: #e3f2fd;
  border-color: #bbdefb;
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(25,118,210,0.1);
}

.navbar-end .button.is-small {
  padding: 0.35rem 0.9rem;
  font-size: 0.92rem;
  border-radius: 0.6rem;
  white-space: nowrap;
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(220,53,69,0.2);
  transition: all 0.2s ease;
  border: none;
}

.navbar-end .button.is-small:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220,53,69,0.25);
}

.auth-actions {
  display: flex;
  gap: 0.7rem;
}

.auth-actions .button {
  padding: 0.4rem 1rem;
  font-size: 0.95rem;
  border-radius: 0.6rem;
  font-weight: 600;
  border: none;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.auth-actions .button.is-light {
  background-color: #f8fafc;
  color: #5a6888;
}

.auth-actions .button.is-primary {
  background-color: #42b983;
  color: white;
}

.auth-actions .button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

@media (max-width: 1024px) {
  .navbar {
    padding: 0.8rem 1.5rem;
  }
  
  .navbar-brand .brand-text {
    font-size: 1.6rem;
  }
  
  .brand-title {
    font-size: 1.6rem;
  }
  
  .navbar-item {
    padding: 0.5rem 0.9rem;
    font-size: 0.95rem;
  }
  
  .admin-link {
    font-size: 0.85rem;
    padding: 0.25rem 0.5rem;
  }
}

@media (max-width: 900px) {
  .navbar-container {
    grid-template-columns: 1fr;
    gap: 0.8rem;
  }
  
  .navbar-brand, .navbar-menu, .navbar-end {
    justify-content: center;
  }
  
  .navbar-menu {
    padding-left: 0;
  }
  
  .user-info {
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.7rem;
  }
  
  .admin-links {
    order: 1;
    width: 100%;
    justify-content: center;
    margin-bottom: 0.6rem;
  }
}

@media (max-width: 600px) {
  .navbar {
    padding: 0.7rem 1rem;
    border-radius: 0 0 18px 18px;
  }

  .navbar-brand .brand-text {
    font-size: 1.4rem;
    padding: 0.2rem 0.4rem 0.2rem 0.2rem;
  }
  
  .brand-logo-wrapper {
    width: 38px;
    height: 38px;
    margin-right: 8px;
  }
  
  .brand-logo {
    width: 26px;
    height: 26px;
  }
  
  .brand-title {
    font-size: 1.4rem;
  }
  
  .navbar-menu {
    gap: 0.3rem;
  }
  
  .navbar-item {
    padding: 0.4rem 0.7rem;
    font-size: 0.92rem;
    border-radius: 0.6rem;
  }
  
  .navbar-item:not(:last-child)::after {
    display: none;
  }
  
  .user-info {
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
  
  .user-greeting {
    margin-bottom: 0.4rem;
    font-size: 0.95rem;
    padding: 0.35rem 0.7rem;
  }
  
  .auth-actions {
    display: flex;
    gap: 0.5rem;
  }
  
  .auth-actions .button {
    margin-left: 0;
    padding: 0.3rem 0.6rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 380px) {
  .navbar-brand .brand-text {
    font-size: 1.3rem;
  }
  
  .brand-title {
    font-size: 1.3rem;
  }
  
  .brand-logo-wrapper {
    width: 34px;
    height: 34px;
    margin-right: 6px;
  }
  
  .navbar-item {
    font-size: 0.88rem;
    padding: 0.3rem 0.6rem;
  }
  
  .user-greeting {
    font-size: 0.9rem;
    padding: 0.3rem 0.6rem;
  }
  
  .admin-link {
    font-size: 0.8rem;
    padding: 0.2rem 0.4rem;
  }
  
  .navbar-end .button.is-small {
    font-size: 0.85rem;
  }
}
</style>