<template>
  <div class="login-page auth-form-container">
    <h2>用户登录</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">用户名或邮箱</label>
        <input id="username" v-model="formData.username" placeholder="用户名或邮箱" required />
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input id="password" v-model="formData.password" type="password" placeholder="密码" required />
      </div>
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? '登录中...' : '登录' }}
      </button>
    </form>
    <p v-if="error" class="error-message">{{ error }}</p>
    <p class="switch-auth">
      还没有账户? <router-link to="/register">立即注册</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';

const store = useStore();
const router = useRouter();
const route = useRoute(); // To get redirect query param

const formData = reactive({
  username: '', // 后端通常允许用户名或邮箱登录
  password: ''
});
const isLoading = ref(false);
const error = computed(() => store.getters['user/authError']);

const handleSubmit = async () => {
  isLoading.value = true;
  store.commit('user/CLEAR_ERROR');
  try {
    await store.dispatch('user/loginUser', {
      username: formData.username, // DRF Token Auth 使用 username
      password: formData.password
    });
    // 登录成功后，跳转到之前的页面或首页
    const redirectPath = route.query.redirect || '/home';
    router.push(redirectPath);
  } catch (err) {
    console.error('Login failed in component:', err.message);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* 移除: @import './RegisterPage.vue'; */

/* 如果需要，将 RegisterPage.vue 中共享的样式直接复制粘贴到这里，
   或者最好是创建一个共享的 CSS 文件并在 App.vue 或 main.js 中全局引入 */

/* 登录页美化样式 */

.auth-form-container {
  max-width: 400px;
  margin: 60px auto 0 auto;
  padding: 36px 32px 28px 32px;
  background: linear-gradient(120deg, #e3f0ff 0%, #f8fafc 100%);
  border-radius: 18px;
  box-shadow: 0 8px 32px rgba(21, 101, 192, 0.13);
  border: 1.5px solid #e3f2fd;
  transition: box-shadow 0.2s;
}

.auth-form-container h2 {
  text-align: center;
  margin-bottom: 28px;
  color: #1976d2;
  font-weight: 800;
  font-size: 2rem;
  letter-spacing: 2px;
  text-shadow: 0 2px 12px rgba(21,101,192,0.08);
}

.form-group {
  margin-bottom: 22px;
}

.form-group label {
  display: block;
  margin-bottom: 7px;
  font-weight: 700;
  color: #1565c0;
  letter-spacing: 1px;
}

.form-group input {
  width: 400px; /* 固定宽度 */
  max-width: 100%; /* 防止溢出容器 */
  box-sizing: border-box; /* 包含内边距和边框 */
  padding: 12px 14px;
  border: 1.5px solid #bbdefb;
  border-radius: 7px;
  font-size: 1.08rem;
  background: #fafdff;
  transition: border 0.2s, box-shadow 0.2s;
  outline: none;
}

.form-group input:focus {
  border-color: #1976d2;
  box-shadow: 0 2px 8px rgba(25,118,210,0.08);
}

.auth-form-container button {
  width: 100%;
  padding: 13px 0;
  background: linear-gradient(90deg, #1976d2 0%, #42b983 100%);
  color: #fff;
  font-weight: 700;
  font-size: 1.1rem;
  border: none;
  border-radius: 7px;
  box-shadow: 0 2px 8px rgba(25,118,210,0.10);
  cursor: pointer;
  transition: background 0.18s, box-shadow 0.18s, transform 0.15s;
}

.auth-form-container button:disabled {
  background: #b0bec5;
  cursor: not-allowed;
  box-shadow: none;
}

.auth-form-container button:hover:not(:disabled) {
  background: linear-gradient(90deg, #1565c0 0%, #2ecc71 100%);
  transform: translateY(-2px) scale(1.03);
}

.error-message {
  color: #e53935;
  background: #fff3f3;
  border: 1px solid #ffcdd2;
  border-radius: 6px;
  padding: 10px 0;
  margin: 18px 0 0 0;
  text-align: center;
  font-size: 1rem;
}

.switch-auth {
  text-align: center;
  margin-top: 24px;
  font-size: 1em;
  color: #888;
}

.switch-auth a {
  color: #1976d2;
  text-decoration: none;
  font-weight: 700;
  margin-left: 4px;
  transition: color 0.18s;
}

.switch-auth a:hover {
  color: #42b983;
  text-decoration: underline;
}

@media (max-width: 500px) {
  .auth-form-container {
    padding: 18px 6vw 18px 6vw;
    border-radius: 12px;
  }
  .auth-form-container h2 {
    font-size: 1.3rem;
  }

}
</style>