<template>
  <div class="home-page">
    <header class="home-header">
      <h1>{{ isAdminView ? '文章管理 (管理员)' : '发现文章' }}</h1>
      <div class="search-controls">
        <input type="search" v-model="searchQuery" @keyup.enter="performSearch" placeholder="搜索文章..." class="search-input"/>
        <select v-model="selectedCategory" @change="performSearch" class="category-select">
          <option value="">所有分类</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
        <!-- 管理员可以筛选文章状态 -->
        <select v-if="isAdminView" v-model="selectedStatus" @change="performSearch" class="status-select">
          <option value="">所有状态</option>
          <option value="published">已发布</option>
          <option value="draft">草稿</option>
        </select>
        <button @click="performSearch()" class="search-button">搜索</button>
      </div>
      <div class="view-toggle">
        <button @click="viewMode = 'grid'" :class="{active: viewMode === 'grid'}">网格</button>
        <button @click="viewMode = 'list'" :class="{active: viewMode === 'list'}">列表</button>
      </div>
    </header>

    <div v-if="isLoading" class="loading-indicator">加载文章中...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="!isLoading && !error && articles.length === 0" class="no-articles">
      <p>没有找到相关文章。</p>
    </div>

    <div :class="['articles-container', viewMode === 'grid' ? 'grid-view' : 'list-view']">
      <div v-for="article in articles" :key="article.id" class="article-item-wrapper">
        <ArticleCard :article="article" />
        <!-- 为管理员在文章卡片旁边添加删除按钮 -->
        <button
          v-if="isAdminView"
          @click="handleDeleteArticle(article.id)"
          class="delete-article-btn-list"
          :disabled="isDeleting === article.id"
        >
          {{ isDeleting === article.id ? '删除中...' : '删除' }}
        </button>
      </div>
    </div>

    <div v-if="pagination.totalPages > 1" class="pagination-controls">
      <button @click="changePage(pagination.currentPage - 1)" :disabled="!pagination.previous">上一页</button>
      <span>第 {{ pagination.currentPage }} / {{ pagination.totalPages }} 页</span>
      <button @click="changePage(pagination.currentPage + 1)" :disabled="!pagination.next">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import ArticleCard from '@/components/ArticleCard.vue';

const store = useStore();

const searchQuery = ref('');
const selectedCategory = ref('');
const selectedStatus = ref(''); // 新增：用于管理员筛选状态，默认为空字符串（所有）
const viewMode = ref('grid');
const isDeleting = ref(null); // 用于跟踪哪个文章正在被删除

const articles = computed(() => store.getters['article/allArticles']);
const categories = computed(() => store.getters['article/allCategories']);
const isLoading = computed(() => store.getters['article/articleIsLoading']);
const error = computed(() => store.getters['article/articleError']);
const pagination = computed(() => store.getters['article/articlePagination']);
const currentUser = computed(() => store.getters['user/currentUser']);
const isAdminView = computed(() => currentUser.value && currentUser.value.is_staff); // 判断是否是管理员视图

const fetchInitialData = async () => {
  store.dispatch('article/fetchCategories');
  performSearch(1);
};

const performSearch = (page = 1) => {
  let statusToFetch = 'published'; // 普通用户默认只看已发布的
  if (isAdminView.value) {
    statusToFetch = selectedStatus.value || ''; // 管理员看所有或按选择的状态，空字符串代表所有
  }

  store.dispatch('article/fetchArticles', {
    search: searchQuery.value,
    category: selectedCategory.value,
    status: statusToFetch,
    page: page
    // 后端 ArticleViewSet 的 get_queryset 需要调整以支持管理员查看所有状态
  });
};

const changePage = (newPage) => {
  if (newPage >= 1 && newPage <= pagination.value.totalPages) {
    performSearch(newPage);
  }
};

const handleDeleteArticle = async (articleId) => {
  if (!isAdminView.value) return; // 再次确认是管理员操作
  if (!confirm(`确定要删除这篇文章 (ID: ${articleId}) 吗？`)) return;
  isDeleting.value = articleId;
  try {
    await store.dispatch('article/deleteArticle', articleId);
    // 如果删除的是当前页的最后一篇文章，并且不是第一页，可以考虑返回上一页
    if (articles.value.length === 0 && pagination.value.currentPage > 1) {
      performSearch(pagination.value.currentPage - 1);
    } else {
      // 否则重新加载当前页或让 Vuex 的列表更新自动生效
      // performSearch(pagination.value.currentPage); // 可以强制刷新当前页
    }
  } catch (err) {
    console.error('Failed to delete article from list:', err);
    // 可以显示错误提示
  } finally {
    isDeleting.value = null;
  }
};

onMounted(() => {
  fetchInitialData();
});
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
.article-item-wrapper {
  position: relative; /* 为了删除按钮的定位（如果需要绝对定位） */
  /* 或者使用 flex/grid 布局 */
  display: flex; /* 如果是列表视图，可以这样让按钮在旁边 */
  flex-direction: column; /* 默认堆叠，网格视图下可能需要调整 */
  align-items: center; /* 示例 */
}
.articles-container.list-view .article-item-wrapper {
  flex-direction: row; /* 列表视图下，卡片和按钮同行 */
  align-items: flex-start; /* 或者 center */
  margin-bottom: 15px;
}
.articles-container.list-view .article-card {
  flex-grow: 1; /* 卡片占据主要空间 */
}

.delete-article-btn-list {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  margin-top: 10px; /* 网格视图下的间距 */
}
.articles-container.list-view .delete-article-btn-list {
  margin-top: 0; /* 列表视图下与卡片顶部对齐 */
  margin-left: 10px; /* 与卡片的间距 */
  align-self: center; /* 垂直居中 */
}

.delete-article-btn-list:disabled {
  background-color: #ccc;
}
.status-select {
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 120px;
}
</style>