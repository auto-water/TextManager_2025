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
          <span class="user-greeting">你好, {{ currentUser.username }}</span>
          <div class="user-dropdown">
            <button class="user-avatar-btn" @click="toggleDropdown">
              <div class="user-avatar">
                <span>{{ currentUser.username.charAt(0).toUpperCase() }}</span>
              </div>
            </button>
            <!-- 将下拉菜单移动到App根元素，避免被其他组件的z-index影响 -->
            <teleport to="body">
              <div class="dropdown-menu" :class="{ 'show': isDropdownOpen }" :style="dropdownPosition">
                <div v-if="isAdmin" class="admin-links">
                  <router-link to="/categories" class="dropdown-item" @click="closeDropdown">
                    分类管理
                  </router-link>
                  <router-link to="/admin/users" class="dropdown-item" @click="closeDropdown">
                    用户管理
                  </router-link>
                </div>
                <div class="dropdown-divider"></div>
                <button @click="handleLogout" class="dropdown-item logout-item">
                  登出
                </button>
              </div>
            </teleport>
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
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();
const isDropdownOpen = ref(false);
const dropdownPosition = ref({});

const isAuthenticated = computed(() => store.getters['user/isAuthenticated']);
const currentUser = computed(() => store.getters['user/currentUser']);
const isAdmin = computed(() => store.getters['user/isAdmin']);

const toggleDropdown = async () => {
  isDropdownOpen.value = !isDropdownOpen.value;
  
  // 如果打开了下拉菜单，计算位置
  if (isDropdownOpen.value) {
    await nextTick();
    const btnElement = document.querySelector('.user-avatar-btn');
    if (btnElement) {
      const rect = btnElement.getBoundingClientRect();
      dropdownPosition.value = {
        position: 'fixed',
        top: `${rect.bottom + 8}px`,
        right: `${window.innerWidth - rect.right}px`
      };
    }
  }
};

const closeDropdown = () => {
  isDropdownOpen.value = false;
};

// 点击页面任何地方关闭下拉菜单
const closeDropdownOnOutsideClick = (event) => {
  const dropdown = document.querySelector('.dropdown-menu');
  const avatarBtn = document.querySelector('.user-avatar-btn');
  if (
    isDropdownOpen.value && 
    dropdown && 
    avatarBtn && 
    !dropdown.contains(event.target) && 
    !avatarBtn.contains(event.target)
  ) {
    closeDropdown();
  }
};

// 在组件挂载时添加全局点击事件监听器
onMounted(() => {
  document.addEventListener('click', closeDropdownOnOutsideClick);
});

// 在组件卸载时清除事件监听器
onBeforeUnmount(() => {
  document.removeEventListener('click', closeDropdownOnOutsideClick);
});

const handleLogout = async () => {
  try {
    await store.dispatch('user/logoutUser');
    closeDropdown();
    router.push('/login');
  } catch (error) {
    console.error('Logout failed:', error);
  }
};
</script>

<style>
/* 全局样式，确保下拉菜单在所有内容之上 */
.dropdown-menu {
  position: fixed !important; /* 使用fixed定位，确保相对于视口 */
  z-index: 9999 !important; /* 非常高的z-index */
  background: white;
  min-width: 180px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: opacity 0.25s ease, visibility 0.25s ease, transform 0.25s ease;
  overflow: hidden;
}

.dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}
</style>

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

/* 用户信息和下拉菜单样式 */
.user-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-greeting {
  color: #1976d2;
  font-weight: 700;
  font-size: 1.05rem;
  white-space: nowrap;
  padding: 0.4rem 0;
}

.user-dropdown {
  position: relative;
  display: inline-block;
}

.user-avatar-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  position: relative;
}

.user-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1976d2, #42b983);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.1rem;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.25);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.user-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 3px 12px rgba(25, 118, 210, 0.3);
}

.dropdown-menu {
  position: fixed !important; /* 使用fixed定位，确保相对于视口 */
  z-index: 9999 !important; /* 非常高的z-index */
  background: white;
  min-width: 180px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: opacity 0.25s ease, visibility 0.25s ease, transform 0.25s ease;
  overflow: hidden;
}

.dropdown-menu.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-item {
  display: flex;
  justify-content: center;
  align-items: center; /* 添加垂直居中 */
  padding: 12px 16px;
  color: #495057;
  text-decoration: none;
  transition: all 0.2s;
  cursor: pointer;
  border: none;
  background: transparent;
  width: 100%;
  box-sizing: border-box; /* 确保内边距包含在宽度内 */
  font-size: 0.95rem;
}

.dropdown-icon {
  margin-right: 10px;
  font-style: normal;
  font-size: 1.1rem;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  color: #1976d2;
}

.dropdown-divider {
  height: 1px;
  background-color: #e9ecef;
  margin: 4px 0;
}

.admin-links {
  border-bottom: none;
}

.logout-item {
  color: #dc3545;
}

.logout-item:hover {
  background-color: #fff5f5;
  color: #c82333;
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
    flex-wrap: nowrap; /* 修改为不换行 */
    justify-content: center;
    gap: 0.7rem;
  }
  
  .admin-links {
    order: 0; /* 改变顺序，不再是第一个 */
    width: auto; /* 允许宽度自适应内容 */
    justify-content: center;
    margin-bottom: 0; /* 移除底部边距 */
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
    flex-direction: row; /* 改为行排列 */
    align-items: center;
    gap: 0.5rem;
    flex-wrap: nowrap; /* 确保不换行 */
  }
  
  .user-greeting {
    margin-bottom: 0; /* 移除底部边距 */
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