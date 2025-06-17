<template>
  <div class="drafts-page">
    <h2>我的草稿</h2>

    <div v-if="isLoading" class="loading-indicator">加载草稿中...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="!isLoading && drafts.length === 0 && !error" class="no-drafts">
      <p>你还没有草稿。 <router-link to="/editor">开始写作</router-link></p>
    </div>

    <div v-else class="drafts-list">
      <div v-for="draft in drafts" :key="draft.id" class="draft-item">
        <div class="draft-info">
          <h3 class="draft-title">{{ draft.title || '无标题草稿' }}</h3>
          <p class="draft-meta">
            最后更新: {{ formatDate(draft.updated_at) }} |
            分类: {{ getCategoryName(draft.category) || '未分类' }}
          </p>
        </div>
        <div class="draft-actions">
          <router-link :to="{ name: 'ArticleEditor', params: { id: draft.id } }" class="action-button edit">
            编辑
          </router-link>
          <button @click="deleteDraft(draft.id)" class="action-button delete" :disabled="isDeleting === draft.id">
            {{ isDeleting === draft.id ? '删除中...' : '删除' }}
          </button>
        </div>
      </div>
    </div>
     <!-- Pagination if needed, assuming fetchArticles in store handles pagination for drafts -->
     <div v-if="pagination.totalPages > 1 && drafts.length > 0" class="pagination-controls">
        <button @click="changePage(pagination.currentPage - 1)" :disabled="!pagination.previous">上一页</button>
        <span>第 {{ pagination.currentPage }} / {{ pagination.totalPages }} 页</span>
        <button @click="changePage(pagination.currentPage + 1)" :disabled="!pagination.next">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router'; // useRouter might not be needed here unless for programmatic nav

const store = useStore();
const isDeleting = ref(null); // Store ID of draft being deleted

// Corrected: drafts should come from allArticles, filtered by status='draft'
// The fetchDrafts function will dispatch fetchArticles with status='draft'
const drafts = computed(() => store.getters['article/allArticles']);
const categories = computed(() => store.getters['article/allCategories']); // For displaying category name
const isLoading = computed(() => store.getters['article/articleIsLoading']);
const error = computed(() => store.getters['article/articleError']);
const pagination = computed(() => store.getters['article/articlePagination']);
// const currentUser = computed(() => store.getters['user/currentUser']); // Not strictly needed if backend filters by user

const fetchDraftsPageData = (page = 1) => {
  // Fetch categories if not already loaded or needed for display logic
  if (categories.value.length === 0) {
    store.dispatch('article/fetchCategories');
  }
  // Fetch draft articles for the current user
  store.dispatch('article/fetchArticles', {
    status: 'draft',
    page: page,
    author: 'me' // 添加author=me参数，确保即使是管理员也只能看到自己的草稿
    // Backend should automatically filter by request.user for drafts
  });
};

onMounted(() => {
  fetchDraftsPageData(1); // Load first page of drafts
});

const deleteDraft = async (draftId) => {
  if (!confirm('确定要删除这篇草稿吗？')) return;
  isDeleting.value = draftId;
  try {
    await store.dispatch('article/deleteArticle', draftId);
    // List will update via Vuex. If current page becomes empty, consider fetching previous page.
    if (drafts.value.length === 0 && pagination.value.currentPage > 1) {
        fetchDraftsPageData(pagination.value.currentPage - 1);
    }
  } catch (err) {
    console.error('Failed to delete draft:', err);
    // Display error to user if needed, Vuex store might already handle it
  } finally {
    isDeleting.value = null;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '未知日期';
  return new Date(dateString).toLocaleString();
};

const getCategoryName = (categoryId) => {
  const category = categories.value.find(cat => cat.id === categoryId);
  return category ? category.name : '未分类';
};

const changePage = (newPage) => {
  if (newPage >= 1 && newPage <= pagination.value.totalPages) {
    fetchDraftsPageData(newPage);
  }
};
</script>

<style scoped>
.drafts-page {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
}
.drafts-page h2 {
  text-align: center;
  margin-bottom: 30px;
}
.no-drafts {
  text-align: center;
  padding: 30px;
  font-size: 1.1em;
  color: #666;
}
.drafts-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.draft-item {
  background-color: #fff;
  padding: 15px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.draft-info .draft-title {
  margin: 0 0 5px 0;
  font-size: 1.2em;
  color: #333;
  cursor: pointer; /* Optional: if title click also navigates to editor */
}
.draft-info .draft-title:hover {
  text-decoration: underline; /* Optional */
}
.draft-info .draft-meta {
  font-size: 0.9em;
  color: #777;
  margin: 0;
}
.draft-actions {
  display: flex;
  gap: 10px;
}
.action-button {
  padding: 6px 12px;
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.9em;
  cursor: pointer;
  border: 1px solid transparent;
  min-width: 60px; /* 确保最小宽度相同 */
  width: 60px; /* 固定宽度，确保两个按钮完全相同宽度 */
  text-align: center; /* 文本居中 */
  display: inline-flex; /* 使用inline-flex替代inline-block */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 32px; /* 固定高度 */
  box-sizing: border-box; /* 确保内边距和边框包含在宽度内 */
  font-weight: normal; /* 统一字重 */
  transition: background-color 0.2s; /* 统一过渡效果 */
  margin: 0; /* 移除所有外边距 */
  vertical-align: middle; /* 垂直对齐 */
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
}
</style>