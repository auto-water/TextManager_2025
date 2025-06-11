<template>
  <footer class="app-footer">
    <p>© {{ new Date().getFullYear() }} 文章管理器. All rights reserved.</p>
    <p>Powered by Vue.js & Django</p>
  </footer>
</template>

<script setup>
// No script needed for this simple footer
</script>

<style scoped>
.app-footer {
  text-align: center;
  padding: 20px;
  background-color: #333;
  color: #fff;
  font-size: 0.9em;
}
.app-footer p {
  margin: 5px 0;
}
</style>