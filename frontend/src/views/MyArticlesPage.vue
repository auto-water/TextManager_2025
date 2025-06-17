<template>
  <div class="my-articles-page">
    <h2>我的已发布文章</h2>

    <div v-if="isLoading" class="loading-indicator">加载文章中...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="!isLoading && articles.length === 0 && !error" class="no-articles">
      <p>你还没有发布文章。 <router-link to="/editor">开始写作</router-link></p>
    </div>

    <div v-else class="articles-list">
      <div v-for="article in articles" :key="article.id" class="article-item">
        <div class="article-info">
          <h3 class="article-title">{{ article.title }}</h3>
          <p class="article-meta">
            发布于: {{ formatDate(article.created_at) }} |
            分类: {{ getCategoryName(article.category) || '未分类' }} |
            {{ article.updated_at !== article.created_at ? '已更新' : '首次发布' }}
          </p>
        </div>
        <div class="article-actions">
          <router-link :to="{ name: 'ArticleDetail', params: { id: article.id } }" class="action-button view">
            查看
          </router-link>
          <router-link :to="{ name: 'ArticleEditor', params: { id: article.id } }" class="action-button edit">
            编辑
          </router-link>
          <button @click="deleteArticle(article.id)" class="action-button delete" :disabled="isDeleting === article.id">
            {{ isDeleting === article.id ? '删除中...' : '删除' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- 分页控制 -->
    <div v-if="pagination.totalPages > 1 && articles.length > 0" class="pagination-controls">
      <button @click="changePage(pagination.currentPage - 1)" :disabled="!pagination.previous">上一页</button>
      <span>第 {{ pagination.currentPage }} / {{ pagination.totalPages }} 页</span>
      <button @click="changePage(pagination.currentPage + 1)" :disabled="!pagination.next">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

const store = useStore();
const isDeleting = ref(null); // 存储正在删除的文章ID

const articles = computed(() => store.getters['article/allArticles']);
const categories = computed(() => store.getters['article/allCategories']);
const isLoading = computed(() => store.getters['article/articleIsLoading']);
const error = computed(() => store.getters['article/articleError']);
const pagination = computed(() => store.getters['article/articlePagination']);

// 加载文章数据的函数
const fetchMyArticles = (page = 1) => {
  // 确保分类数据已加载
  if (categories.value.length === 0) {
    store.dispatch('article/fetchCategories');
  }
  
  // 修复：明确传递 author='me' 参数作为对象的属性
  store.dispatch('article/fetchArticles', {
    status: 'published',
    author: 'me', // 传递这个关键参数，指示后端只获取当前用户的文章
    page: page
  });
};

onMounted(() => {
  fetchMyArticles(1); // 加载第一页文章
});

// 删除文章的处理函数
const deleteArticle = async (articleId) => {
  if (!confirm('确定要删除这篇文章吗？此操作不可撤销。')) return;
  isDeleting.value = articleId;
  
  try {
    await store.dispatch('article/deleteArticle', articleId);
    // 如果当前页面已空且不是第一页，获取前一页数据
    if (articles.value.length === 0 && pagination.value.currentPage > 1) {
      fetchMyArticles(pagination.value.currentPage - 1);
    } else if (articles.value.length === 0) {
      // 如果是第一页且删除后为空，重新加载第一页
      fetchMyArticles(1);
    }
  } catch (err) {
    console.error('Failed to delete article:', err);
  } finally {
    isDeleting.value = null;
  }
};

// 日期格式化函数
const formatDate = (dateString) => {
  if (!dateString) return '未知日期';
  return new Date(dateString).toLocaleString();
};

// 获取分类名称的辅助函数
const getCategoryName = (categoryId) => {
  const category = categories.value.find(cat => cat.id === categoryId);
  return category ? category.name : '未分类';
};

// 分页处理
const changePage = (newPage) => {
  if (newPage >= 1 && newPage <= pagination.value.totalPages) {
    fetchMyArticles(newPage);
  }
};
</script>

<style scoped>
.my-articles-page {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
}
.my-articles-page h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
  font-weight: 600;
}
.no-articles {
  text-align: center;
  padding: 30px;
  font-size: 1.1em;
  color: #666;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.articles-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.article-item {
  background-color: #fff;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}
.article-info {
  flex: 1;
  min-width: 200px;
}
.article-info .article-title {
  margin: 0 0 8px 0;
  font-size: 1.2em;
  color: #2c3e50;
  font-weight: 600;
}
.article-info .article-meta {
  font-size: 0.85em;
  color: #6c757d;
  margin: 0;
}
.article-actions {
  display: flex;
  gap: 8px;
  margin-top: 10px;
  flex-wrap: wrap;
}
.action-button {
  padding: 6px 12px;
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.9em;
  cursor: pointer;
  border: 1px solid transparent;
  min-width: 60px;
  width: 60px;
  text-align: center;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  height: 32px;
  box-sizing: border-box;
  font-weight: normal;
  transition: background-color 0.2s;
  margin: 0;
  vertical-align: middle;
}
.action-button.view {
  background-color: #17a2b8;
  color: white;
}
.action-button.view:hover {
  background-color: #138496;
}
.action-button.edit {
  background-color: #42b983;
  color: white;
}
.action-button.edit:hover {
  background-color: #3aa875;
}
.action-button.delete {
  background-color: #f14668;
  color: white;
}
.action-button.delete:hover {
  background-color: #ee3058;
}
.action-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.loading-indicator, .error-message {
  text-align: center;
  padding: 20px;
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
  background-color: #e9ecef;
  border: 1px solid #dee2e6;
  color: #495057;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}
.pagination-controls button:hover:not(:disabled) {
  background-color: #dae0e5;
}
.pagination-controls button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .article-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .article-actions {
    width: 100%;
    justify-content: flex-start;
    margin-top: 15px;
  }
}
</style>
