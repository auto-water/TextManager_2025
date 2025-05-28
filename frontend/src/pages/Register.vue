<template>
    <div>
      <h2>注册</h2>
      <input v-model="username" placeholder="用户名" />
      <input v-model="password" placeholder="密码" type="password" />
      <button @click="register">注册</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import api from '../api'
  
  const username = ref('')
  const password = ref('')
  
  const register = async () => {
    const res = await api.post('register/', {
      username: username.value,
      password: password.value,
    })
    console.log('注册成功，Token:', res.data)
  }
  </script>
  