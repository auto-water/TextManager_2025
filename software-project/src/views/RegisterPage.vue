<template>
  <div class="register-page auth-form-container">
    <h2>用户注册</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="username">用户名</label>
        <input id="username" v-model="formData.username" placeholder="用户名" required />
      </div>
      <div class="form-group">
        <label for="email">邮箱</label>
        <input id="email" v-model="formData.email" type="email" placeholder="邮箱" required />
      </div>
      <div class="form-group">
        <label for="password">密码</label>
        <input id="password" v-model="formData.password" type="password" placeholder="密码" required />
      </div>
      <div class="form-group">
        <label for="passwordConfirm">确认密码</label>
        <input id="passwordConfirm" v-model="formData.passwordConfirm" type="password" placeholder="确认密码" required />
      </div>
      <button type="submit" :disabled="isLoading">
        {{ isLoading ? '注册中...' : '注册' }}
      </button>
    </form>
    <p v-if="error" class="error-message">{{ error }}</p>
    <p class="switch-auth">
      已有账户? <router-link to="/login">立即登录</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';

const store = useStore();
const router = useRouter();

const formData = reactive({
  username: '',
  email: '',
  password: '',
  passwordConfirm: ''
});
const isLoading = ref(false);

// Use a computed property to get the error from Vuex
const error = computed(() => store.getters['user/authError']);

const handleSubmit = async () => {
  // 前端的密码一致性检查仍然保留，这是一个好的用户体验
  if (formData.password !== formData.passwordConfirm) {
    store.commit('user/SET_ERROR', '两次输入的密码不一致');
    return;
  }
  isLoading.value = true;
  store.commit('user/CLEAR_ERROR'); // Clear previous errors

  try {
    await store.dispatch('user/registerUser', {
      username: formData.username,
      email: formData.email,
      password: formData.password,
      password2: formData.passwordConfirm // <--- 修改这里：添加 password2 字段
    });
    // 注册成功后，可以提示用户去登录，或者根据后端逻辑跳转
    alert('注册成功！请登录。'); // 简单的提示
    router.push('/login');
  } catch (err) {
    // Error is already set in Vuex action, so just log it or do nothing
    console.error('Registration failed in component:', err.message);
    // 注意：err.message 现在可能就是后端返回的 JSON 字符串，
    // Vuex action 中应该更好地处理它，将其解析为可读的错误信息。
    // 如果 store.getters['user/authError'] 已经是处理过的字符串，那么这里就不需要额外处理。
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Shared styles for auth forms */
.auth-form-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.auth-form-container h2 {
  text-align: center;
  margin-bottom: 25px;
  color: #333;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}
.auth-form-container button {
  width: 100%;
  padding: 12px;
}
.switch-auth {
  text-align: center;
  margin-top: 20px;
  font-size: 0.9em;
}
.switch-auth a {
  color: #42b983;
  text-decoration: none;
}
.switch-auth a:hover {
  text-decoration: underline;
}
</style>