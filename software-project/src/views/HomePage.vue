<template>
  <div class="home-page">
    <header class="home-header">
      <h1>{{ isAdminView ? '文章管理 (管理员)' : '发现文章' }}</h1>
      <div class="search-controls">
        <input
          type="search"
          v-model="searchQuery"
          @keyup.enter="performSearch(1)"
          placeholder="搜索文章标题、内容..."
          class="search-input"
        />
        <!-- 使用新的 categoriesForSelect getter -->
        <select v-model="selectedCategory" @change="performSearch(1)" class="category-select">
          <option value="">所有分类</option>
          <!-- 遍历处理过的带有层级前缀的分类列表 -->
          <option v-for="cat in formattedCategories" :key="cat.id" :value="cat.id">
            {{ cat.name }} <!-- cat.name 现在已经包含了缩进前缀 -->
          </option>
        </select>
        <!-- 管理员可以筛选文章状态 -->
        <select v-if="isAdminView" v-model="selectedStatus" @change="performSearch(1)" class="status-select">
          <option value="">所有状态</option>
          <option value="published">已发布</option>
          <option value="draft">草稿</option>
        </select>
        <button @click="performSearch(1)" class="button search-button">搜索</button>
      </div>
      <div class="view-toggle">
        <button @click="viewMode = 'grid'" :class="{active: viewMode === 'grid'}">网格视图</button>
        <button @click="viewMode = 'list'" :class="{active: viewMode === 'list'}">列表视图</button>
      </div>
    </header>

    <!-- ... (rest of the template remains the same) ... -->
    <div v-if="isLoading" class="loading-indicator">
      <p>加载文章中...</p>
    </div>
    <div v-if="error" class="error-message">
      <p>加载文章失败: {{ error }}</p>
    </div>
    <div v-if="!isLoading && !error && articles.length === 0" class="no-articles">
      <p>没有找到相关文章。尝试更换搜索词或分类。</p>
      <router-link v-if="!isAdminView" to="/editor" class="button is-primary">去写一篇</router-link>
    </div>
    <div :class="['articles-container', viewMode === 'grid' ? 'grid-view' : 'list-view']">
      <div v-for="article in articles" :key="article.id" class="article-item-wrapper">
        <ArticleCard :article="article" />
        <button
          v-if="isAdminView"
          @click="handleDeleteArticle(article.id)"
          class="button is-danger is-small delete-article-btn-list"
          :disabled="isDeleting === article.id"
        >
          {{ isDeleting === article.id ? '删除中...' : '删除' }}
        </button>
      </div>
    </div>
    <div v-if="!isLoading && articles.length > 0 && pagination.totalPages > 1" class="pagination-controls">
      <button @click="changePage(pagination.currentPage - 1)" :disabled="!pagination.previous" class="button">
        « 上一页
      </button>
      <span>第 {{ pagination.currentPage }} / {{ pagination.totalPages }} 页</span>
      <button @click="changePage(pagination.currentPage + 1)" :disabled="!pagination.next" class="button">
        下一页 »
      </button>
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
const selectedStatus = ref('');
const viewMode = ref('grid');
const isDeleting = ref(null);

const articles = computed(() => store.getters['article/allArticles']);
// 使用新的 getter 来获取格式化后的分类列表
const formattedCategories = computed(() => store.getters['category/categoriesForSelect']);
// 如果你的分类数据仍在 article 模块，则使用:
// const formattedCategories = computed(() => store.getters['article/categoriesForSelect']);

const isLoading = computed(() => store.getters['article/articleIsLoading'] || store.getters['category/categoryIsLoading']); // 包含分类加载状态
const error = computed(() => store.getters['article/articleError'] || store.getters['category/categoryError']); // 包含分类错误状态
const pagination = computed(() => store.getters['article/articlePagination']);
const currentUser = computed(() => store.getters['user/currentUser']);
const isAdminView = computed(() => currentUser.value && currentUser.value.is_staff);

const fetchInitialData = async () => {
  // 根据你的 store 模块名调整
  store.dispatch('category/fetchCategories'); // 或者 'article/fetchCategories'
  performSearch(1);
};

const performSearch = (page = 1) => {
  let statusToFetch = 'published';
  if (isAdminView.value) {
    statusToFetch = selectedStatus.value || '';
  }

  store.dispatch('article/fetchArticles', {
    search: searchQuery.value,
    category: selectedCategory.value,
    status: statusToFetch,
    page: Number(page)
  });
};

const changePage = (newPage) => {
  if (newPage >= 1 && newPage <= pagination.value.totalPages) {
    performSearch(newPage);
  }
};

const handleDeleteArticle = async (articleId) => {
  if (!isAdminView.value) return;
  if (!confirm(`确定要删除这篇文章 (ID: ${articleId}) 吗？此操作不可撤销。`)) return;
  isDeleting.value = articleId;
  try {
    await store.dispatch('article/deleteArticle', articleId);
    if (articles.value.length === 0 && pagination.value.currentPage > 1) {
      performSearch(pagination.value.currentPage - 1);
    } else if (articles.value.length === 0 && pagination.value.currentPage === 1) {
      performSearch(1);
    }
  } catch (err) {
    console.error('Failed to delete article from list:', err);
    store.commit('article/SET_ERROR', '删除文章失败，请重试。');
  } finally {
    isDeleting.value = null;
  }
};

onMounted(() => {
  fetchInitialData();
});
</script>

<style scoped>
/* ... (styles remain the same as your provided HomePage.vue) ... */
.home-page {
  /* Padding is handled by .main-content in App.vue */
}

.home-header {
  background-color: #ffffff;
  padding: 2rem 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06); /* Slightly more pronounced shadow */
  margin-bottom: 2.5rem;
  text-align: center;
}

.home-header h1 {
  font-size: 2.25rem;
  color: #2c3e50; /* Darker, more neutral blue-gray */
  margin-bottom: 1.5rem;
  font-weight: 700; /* Bolder */
}

.search-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem; /* Increased gap */
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  max-width: 900px; /* Wider search area */
  margin-left: auto;
  margin-right: auto;
}

/* Using global styles for input, select, button from App.vue */
/* Specific overrides or additions for HomePage if needed */
.search-input {
  min-width: 250px; /* Adjust as needed */
  flex: 1 1 300px; /* Allow flexible growth */
}
.category-select, .status-select {
  min-width: 150px;
  flex: 0 1 200px; /* Don't grow too much */
}
.search-button {
  flex-shrink: 0; /* Prevent button from shrinking */
}

.view-toggle {
  margin-top: 1rem; /* Added margin-top if search controls wrap */
}
.view-toggle button {
  margin: 0 0.4rem;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  /* Using global button styles, .active style below */
}
.view-toggle button.active {
  background-color: #007bff; /* Primary color from global styles */
  color: white;
  border-color: #007bff;
}
.view-toggle button:not(.active) {
    background-color: #e9ecef; /* Light button style from global */
    color: #212529;
    border-color: #dee2e6;
}
.view-toggle button:not(.active):hover {
    background-color: #dae0e5;
}


.articles-container.grid-view {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.article-item-wrapper {
  display: flex;
  flex-direction: column; /* For grid view, card and button stack */
}

.articles-container.list-view .article-item-wrapper {
  flex-direction: row;
  align-items: center; /* Vertically align card and button */
  background-color: #fff;
  border-radius: 0.3rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  padding: 1rem;
  margin-bottom: 1rem; /* Spacing between list items */
}
.articles-container.list-view .article-card {
  flex-grow: 1;
  margin-bottom: 0;
  box-shadow: none;
  border-radius: 0; /* Remove card's own border-radius if wrapper has it */
}

.delete-article-btn-list {
  /* Global .button.is-danger.is-small should apply */
  /* Additional specific styling if needed */
  margin-top: 0.5rem; /* Spacing in grid view */
  align-self: flex-end; /* Align to the right in grid view column */
}
.articles-container.list-view .delete-article-btn-list {
  margin-top: 0;
  margin-left: 1rem; /* Spacing from card in list view */
  align-self: center;
}


.no-articles {
  text-align: center;
  padding: 3rem 1rem;
  color: #6c757d;
  font-size: 1.1rem;
  background-color: #fff;
  border-radius: 0.3rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.no-articles .button {
    margin-top: 1rem;
}

.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2.5rem;
  gap: 0.75rem;
}
.pagination-controls .button {
  /* Using global button styles, ensuring they are light/secondary by default */
   background-color: #e9ecef;
   border-color: #dee2e6;
   color: #212529;
}
.pagination-controls .button:hover:not(:disabled) {
  background-color: #dae0e5;
}
.pagination-controls span {
  font-size: 0.95rem;
  color: #495057;
  padding: 0 0.5rem;
}
</style>