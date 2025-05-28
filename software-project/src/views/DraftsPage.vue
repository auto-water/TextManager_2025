<template>
  <div class="article-detail-page">
    <div v-if="isLoading" class="loading-indicator">加载文章详情...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <article v-if="article && !isLoading" class="article-content-wrapper">
      <header class="article-header">
        <h1>{{ article.title }}</h1>
        <div class="article-meta">
          <span>作者: {{ article.author?.username || '未知' }}</span> |
          <span>发布于: {{ formatDate(article.created_at) }}</span> |
          <span v-if="article.category_details">分类: {{ article.category_details?.name || '未分类' }}</span>
          <span v-if="article.updated_at !== article.created_at"> | 最后更新: {{ formatDate(article.updated_at) }}</span>
        </div>
        <div class="article-actions" v-if="canEditOrDelete">
          <router-link :to="{ name: 'ArticleEditor', params: { id: article.id } }" class="action-btn edit">编辑</router-link>
          <button @click="handleDeleteArticle" class="action-btn delete" :disabled="isDeleting">
            {{ isDeleting ? '删除中...' : '删除' }}
          </button>
        </div>
      </header>

      <div v-if="article.cover_image" class="article-cover-image">
        <img :src="article.cover_image" :alt="article.title">
      </div>
      
      <!-- Using v-html for content from RichTextEditor. Ensure content is sanitized on backend or frontend if from untrusted sources -->
      <div class="article-body" v-html="article.content"></div>
      <!-- If content is markdown, you'd use a markdown renderer here -->

      <hr class="separator" />

      <CommentList :article-id="articleId" />
    </article>

    <div v-if="!article && !isLoading && !error" class="not-found">
      <p>文章未找到或无法加载。</p>
      <router-link to="/home">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';
import CommentList from '@/components/CommentList.vue'; // Import comment component

const store = useStore();
const route = useRoute();
const router = useRouter();

const articleId = ref(route.params.id);
const isDeleting = ref(false);

const article = computed(() => store.getters['article/currentArticleDetail']);
const isLoading = computed(() => store.getters['article/articleIsLoading']);
const error = computed(() => store.getters['article/articleError']);
const currentUser = computed(() => store.getters['user/currentUser']);
const isAdmin = computed(() => store.getters['user/isAdmin']);

const canEditOrDelete = computed(() => {
  if (!currentUser.value || !article.value) return false;
  return isAdmin.value || article.value.author?.id === currentUser.value.id;
});

const fetchArticle = (id) => {
  store.dispatch('article/fetchArticleById', id).catch(err => {
    console.error("Failed to load article in component:", err);
    // Error is handled by computed 'error'
  });
};

onMounted(() => {
  fetchArticle(articleId.value);
});

// Watch for route param changes if navigating between article details
watch(() => route.params.id, (newId) => {
  if (newId && newId !== articleId.value) {
    articleId.value = newId;
    fetchArticle(newId);
  }
});

const formatDate = (dateString) => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleString();
};

const handleDeleteArticle = async () => {
  if (!article.value || !confirm('确定要删除这篇文章吗？此操作不可撤销。')) return;
  isDeleting.value = true;
  try {
    await store.dispatch('article/deleteArticle', article.value.id);
    router.push('/home'); // Redirect after deletion
  } catch (err) {
    console.error('Failed to delete article:', err);
    // Display error to user
  } finally {
    isDeleting.value = false;
  }
};

// Make sure to clean up currentArticle when component is unmounted
// or before fetching a new one to avoid showing old data briefly.
// Vuex action for fetchArticleById should set currentArticle to null initially
// or component can do it before dispatching.
// onBeforeUnmount(() => {
//   store.commit('article/SET_CURRENT_ARTICLE', null);
// });
</script>

<style scoped>
.article-detail-page {
  max-width: 800px; /* Or a bit wider for readability */
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.article-header {
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}
.article-header h1 {
  font-size: 2.2em;
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 10px;
  line-height: 1.3;
}
.article-meta {
  font-size: 0.9em;
  color: #7f8c8d;
  margin-bottom: 15px;
}
.article-meta span {
  margin-right: 8px;
}
.article-actions {
  margin-top: 10px;
}
.action-btn {
  margin-right: 10px;
  padding: 6px 12px;
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.9em;
}
.action-btn.edit {
  background-color: #3498db;
  color: white;
  border: none;
}
.action-btn.delete {
  background-color: #e74c3c;
  color: white;
  border: none;
}
.action-btn:disabled {
  background-color: #bdc3c7;
}

.article-cover-image {
  margin-bottom: 25px;
}
.article-cover-image img {
  max-width: 100%;
  height: auto;
  border-radius: 6px;
}

.article-body {
  font-size: 1.1em;
  line-height: 1.7;
  color: #34495e;
  word-wrap: break-word; /* Ensure long words don't break layout */
}
/* Basic styling for HTML content from Rich Text Editor */
.article-body :deep(p) {
  margin-bottom: 1em;
}
.article-body :deep(h1), .article-body :deep(h2), .article-body :deep(h3) {
  margin-top: 1.5em;
  margin-bottom: 0.8em;
  line-height: 1.4;
}
.article-body :deep(ul), .article-body :deep(ol) {
  padding-left: 1.5em;
  margin-bottom: 1em;
}
.article-body :deep(blockquote) {
  margin-left: 0;
  padding-left: 1em;
  border-left: 3px solid #bdc3c7;
  color: #7f8c8d;
  font-style: italic;
}
.article-body :deep(pre), .article-body :deep(code-block) { /* For code blocks from Quill */
  background-color: #f0f0f0;
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
  margin-bottom: 1em;
  font-family: 'Courier New', Courier, monospace;
}
.article-body :deep(img) {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    margin: 1em 0;
}

.separator {
  margin: 40px 0;
  border: 0;
  border-top: 1px solid #eee;
}
.not-found {
  text-align: center;
  padding: 50px 20px;
}
.not-found p {
  font-size: 1.2em;
  color: #e74c3c;
  margin-bottom: 20px;
}
.not-found a {
  color: #3498db;
  text-decoration: none;
}
</style>