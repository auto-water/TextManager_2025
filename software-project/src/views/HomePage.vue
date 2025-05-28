<template>
  <div class="home-page">
    <header class="home-header">
      <h1>发现文章</h1>
      <div class="search-controls">
        <input type="search" v-model="searchQuery" @keyup.enter="performSearch" placeholder="搜索文章标题、内容..." class="search-input"/>
        <select v-model="selectedCategory" @change="performSearch" class="category-select">
          <option value="">所有分类</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
        <button @click="performSearch" class="search-button">搜索</button>
      </div>
      <div class="view-toggle">
        <button @click="viewMode = 'grid'" :class="{active: viewMode === 'grid'}">网格</button>
        <button @click="viewMode = 'list'" :class="{active: viewMode === 'list'}">列表</button>
      </div>
    </header>

    <div v-if="isLoading" class="loading-indicator">加载文章中...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="!isLoading && !error && articles.length === 0" class="no-articles">
      <p>没有找到相关文章。尝试更换搜索词或分类。</p>
    </div>

    <div :class="['articles-container', viewMode === 'grid' ? 'grid-view' : 'list-view']">
      <ArticleCard v-for="article in articles" :key="article.id" :article="article" />
    </div>

    <div v-if="pagination.totalPages > 1" class="pagination-controls">
      <button @click="changePage(pagination.currentPage - 1)" :disabled="!pagination.previous">上一页</button>
      <span>第 {{ pagination.currentPage }} / {{ pagination.totalPages }} 页</span>
      <button @click="changePage(pagination.currentPage + 1)" :disabled="!pagination.next">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import ArticleCard from '@/components/ArticleCard.vue';

const store = useStore();

const searchQuery = ref('');
const selectedCategory = ref(''); // Store category ID
const viewMode = ref('grid'); // 'grid' or 'list'

const articles = computed(() => store.getters['article/allArticles']);
const categories = computed(() => store.getters['article/allCategories']); // Assuming categories are in article module
// If categories are in their own module: computed(() => store.getters['category/allCategories']);
const isLoading = computed(() => store.getters['article/articleIsLoading']);
const error = computed(() => store.getters['article/articleError']);
const pagination = computed(() => store.getters['article/articlePagination']);


const fetchInitialData = async () => {
  store.dispatch('article/fetchCategories'); // Fetch categories for the filter
  performSearch(1); // Fetch articles for page 1
};

const performSearch = (page = 1) => {
  store.dispatch('article/fetchArticles', {
    search: searchQuery.value,
    category: selectedCategory.value,
    status: 'published', // Only show published articles on home
    page: page
  });
};

const changePage = (newPage) => {
  if (newPage >= 1 && newPage <= pagination.value.totalPages) {
    performSearch(newPage);
  }
};

onMounted(() => {
  fetchInitialData();
});

// Optional: watch for query/category changes to auto-search, or rely on button click
// watch([searchQuery, selectedCategory], () => {
//   performSearch(); // This would search on every keystroke/selection change
// });
</script>

<style scoped>
.home-page {
  padding: 20px;
}
.home-header {
  margin-bottom: 30px;
  text-align: center;
}
.home-header h1 {
  font-size: 2.5em;
  color: #333;
  margin-bottom: 20px;
}
.search-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}
.search-input {
  padding: 10px 15px;
  font-size: 1em;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 300px;
  flex-grow: 1;
}
.category-select {
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 150px;
}
.search-button {
  padding: 10px 20px;
}
.view-toggle {
  margin-bottom: 20px;
}
.view-toggle button {
  margin: 0 5px;
  padding: 8px 12px;
  background-color: #eee;
  border: 1px solid #ddd;
  color: #555;
}
.view-toggle button.active {
  background-color: #42b983;
  color: white;
  border-color: #42b983;
}

.articles-container.grid-view {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
.articles-container.list-view .article-card { /* Style for list view if needed */
  margin-bottom: 15px;
  /* Example: Make it wider for list view */
  /* max-width: 800px; */
  /* margin-left: auto; */
  /* margin-right: auto; */
}
.no-articles {
  text-align: center;
  padding: 40px 0;
  color: #777;
  font-size: 1.2em;
}
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
  gap: 10px;
}
.pagination-controls button {
  padding: 8px 15px;
}
.pagination-controls span {
  font-size: 1em;
}
</style>