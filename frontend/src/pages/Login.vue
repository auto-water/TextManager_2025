<template>
    <div>
      <h2>登录</h2>
      <input v-model="username" placeholder="用户名" />
      <input v-model="password" placeholder="密码" type="password" />
      <button @click="login">登录</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import api from '../api'
  
  const username = ref('')
  const password = ref('password')
  
  const login = async () => {
    const res = await api.post('login/', {
      username: username.value,
      password: password.value,
    })
    console.log('登录成功，Token:', res.data)
  }
  </script>
  