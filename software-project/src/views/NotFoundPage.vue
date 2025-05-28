<template>
  <div class="not-found-page">
    <h1>404 - 页面未找到</h1>
    <p>抱歉，您要查找的页面不存在。</p>
    <router-link to="/home">返回首页</router-link>
  </div>
</template>

<script setup>
// No specific script needed for a simple 404 page
</script>

<style scoped>
.not-found-page {
  text-align: center;
  padding: 50px 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}
.not-found-page h1 {
  font-size: 3em;
  color: #e74c3c;
  margin-bottom: 10px;
}
.not-found-page p {
  font-size: 1.2em;
  color: #7f8c8d;
  margin-bottom: 30px;
}
.not-found-page a {
  font-size: 1.1em;
  color: #3498db;
  text-decoration: none;
  padding: 10px 20px;
  border: 1px solid #3498db;
  border-radius: 5px;
  transition: background-color 0.3s, color 0.3s;
}
.not-found-page a:hover {
  background-color: #3498db;
  color: white;
}
</style>