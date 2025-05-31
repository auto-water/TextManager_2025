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

.auth-form-container { /* Copied for clarity for now */
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.auth-form-container h2 { text-align: center; margin-bottom: 25px; color: #333; }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
.auth-form-container button { width: 100%; padding: 12px; }
.switch-auth { text-align: center; margin-top: 20px; font-size: 0.9em; }
.switch-auth a { color: #42b983; text-decoration: none; }
.switch-auth a:hover { text-decoration: underline; }
</style>