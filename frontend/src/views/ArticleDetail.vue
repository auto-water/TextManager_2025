<template>
  <div class="article-detail-page">
    <!-- 1. 加载状态 -->
    <div v-if="isLoading" class="loading-indicator">
      <p>正在加载文章详情...</p>
      <!-- 可以放一个加载动画 -->
    </div>

    <!-- 2. 错误状态 -->
    <div v-else-if="error" class="error-message">
      <p>加载文章失败: {{ error }}</p>
      <router-link to="/home" class="button">返回首页</router-link>
    </div>

    <!-- 3. 成功加载文章数据 -->
    <article v-else-if="article" class="article-content-wrapper">
      <header class="article-header">
        <h1>{{ article.title }}</h1>
        <div class="article-meta">
          <span>作者: {{ article.author?.username || '未知作者' }}</span> |
          <span>发布于: {{ formatDate(article.created_at) }}</span>
          <span v-if="article.category_details"> | 分类: {{ article.category_details?.name || '未分类' }}</span>
          <span v-if="article.updated_at && article.updated_at !== article.created_at"> | 最后更新: {{ formatDate(article.updated_at) }}</span>
        </div>
        <!-- 编辑和删除按钮 -->
        <div class="article-actions" v-if="canEditOrDelete">
          <router-link :to="{ name: 'ArticleEditor', params: { id: article.id } }" class="button is-info is-small">编辑</router-link>
          <button @click="handleDeleteArticle" class="button is-danger is-small" :disabled="isDeleting">
            {{ isDeleting ? '删除中...' : '删除' }}
          </button>
        </div>
      </header>

      <div v-if="article.cover_image" class="article-cover-image">
        <img :src="article.cover_image" :alt="article.title + ' cover image'">
      </div>

      <!-- 文章内容 (确保后端返回的 article.content 是安全的 HTML) -->
      <div class="article-body" v-html="article.content"></div>

      <hr class="separator" />

      <!-- AI摘要按钮 -->
      <div class="ai-summary">
        <button @click="generateAbstract" class="button is-primary is-small">点击生成AI摘要</button>
      </div>

      <!-- 显示生成的摘要 -->
      <div v-if="abstract" class="ai-abstract">
        <h3>AI生成的摘要：</h3>
        <p>{{ abstract }}</p>
      </div>

      <!-- 评论组件 -->
      <CommentList :article-id="articleId" />
    </article>

    <!-- 4. 文章未找到 (article 为 null 且没有错误和加载状态) -->
    <div v-else class="not-found">
      <p>文章未找到或无法加载。</p>
      <router-link to="/home" class="button">返回首页</router-link>
    </div>
  </div>
</template>

<script setup>
// ... (你提供的 script setup 部分，它是正确的) ...
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue';
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import CommentList from '@/components/CommentList.vue';


const store = useStore();
const route = useRoute();
const router = useRouter();

const articleId = ref(route.params.id);
const isDeleting = ref(false);
const abstract = ref(''); // 用于存储生成的摘要

const article = computed(() => store.getters['article/currentArticleDetail']);
const isLoading = computed(() => store.getters['article/articleIsLoading']);
const error = computed(() => store.getters['article/articleError']);
const currentUser = computed(() => store.getters['user/currentUser']);
const isAdmin = computed(() => store.getters['user/isAdmin']);

const canEditOrDelete = computed(() => {
  if (!currentUser.value || !article.value) return false;
  // 修改权限逻辑：只有作者本人可以编辑/删除文章
  return article.value.author?.id === currentUser.value.id;
});

const fetchArticle = (id) => {
  store.dispatch('article/fetchArticleById', id).catch(err => {
    console.error("Failed to load article in component (fetchArticleById catch):", err.message || err);
    // 错误应该由 Vuex action 内部的 commit('SET_ERROR') 处理，并通过 error 计算属性显示
  });
};

onMounted(() => {
  if (articleId.value) {
    fetchArticle(articleId.value);
  } else {
    // 如果没有 articleId (例如直接访问 /articles/ 路径，这是不可能的，因为路由需要id)
    // 但作为防御性编程，可以设置一个错误或重定向
    console.error("ArticleDetail: No article ID found in route params.");
    store.commit('article/SET_ERROR', '无效的文章ID');
    // router.push('/home'); // 或者重定向
  }
});

watch(() => route.params.id, (newId, oldId) => {
  if (newId && newId !== articleId.value) { // 确保 newId 存在且与当前 articleId 不同
    articleId.value = newId;
    fetchArticle(newId);
  } else if (!newId && article.value) {
    store.commit('article/SET_CURRENT_ARTICLE', null);
  }
  // 如果 newId 是 undefined 或 null，并且之前有 articleId，也应该清理
  // onMounted 中已经处理了 articleId.value 存在的情况
}, { immediate: false }); // immediate: false (默认) 避免在初始挂载时重复调用 (onMounted 已处理)


const formatDate = (dateString) => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleString();
};

const handleDeleteArticle = async () => {
  if (!article.value || !confirm('确定要删除这篇文章吗？此操作不可撤销。')) return;
  isDeleting.value = true;
  try {
    await store.dispatch('article/deleteArticle', article.value.id);
    router.push('/home');
  } catch (err) {
    console.error('Failed to delete article:', err);
    store.commit('article/SET_ERROR', '删除文章失败: ' + (err.message || '请重试'));
  } finally {
    isDeleting.value = false;
  }
};

const generateAbstract = async () => {
  if (!article.value || !article.value.content) {
    abstract.value = '无法生成摘要，因为文章内容为空。';
    return;
  }

  try {
    const apiUrl = 'http://localhost:8000/api/generate-summary/';
    const requestBody = {
      content: article.value.content,
    };

    const token = localStorage.getItem('user_token');
    if (!token) {
      abstract.value = '无法生成摘要，用户未登录或 Token 缺失。';
      return;
    }

    const response = await axios.post(apiUrl, requestBody, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
    });

    if (response.data && response.data.summary) {
      abstract.value = response.data.summary;
    } else {
      abstract.value = '无法生成摘要，请稍后重试。';
    }
  } catch (error) {
    console.error('生成摘要失败:', error);
    abstract.value = '生成摘要时发生错误，请稍后重试。';
  }
};

onBeforeUnmount(() => {
  store.commit('article/SET_CURRENT_ARTICLE', null);
});
</script>

<style scoped>
/* AI摘要按钮样式 */
.ai-summary {
  margin-top: 1.5rem;
  text-align: center;
}
/* AI摘要内容样式 */
.ai-abstract {
  margin-top: 1.5rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
.article-detail-page {
  max-width: 800px;
  margin: 20px auto;
  padding: 25px;
  background-color: #fff;
  border-radius: 0.5rem; /* 与其他页面统一 */
  box-shadow: 0 2px 10px rgba(0,0,0,0.07); /* 更统一的阴影 */
}
.article-header {
  margin-bottom: 2rem; /* 增加间距 */
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e9ecef; /* 更浅的分割线 */
}
.article-header h1 {
  font-size: 2.25rem; /* 与 HomePage 标题协调 */
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 0.75rem; /* 调整间距 */
  line-height: 1.3;
  font-weight: 700;
}
.article-meta {
  font-size: 0.9rem;
  color: #6c757d; /* 中性灰色 */
  margin-bottom: 1rem;
}
.article-meta span {
  margin-right: 0.75rem;
}
.article-meta span:last-child {
  margin-right: 0;
}

.article-actions {
  margin-top: 1rem;
  display: flex;
  gap: 0.5rem;
}
/* 按钮样式会继承 App.vue 中的全局 .button 样式 */
.article-actions .button.is-small {
    padding: 0.35rem 0.75rem;
    font-size: 0.875rem;
}
.article-actions .button.is-info { /* 示例：编辑按钮颜色 */
    background-color: #17a2b8;
    border-color: #17a2b8;
    color: white;
}
.article-actions .button.is-info:hover {
    background-color: #138496;
    border-color: #117a8b;
}


.article-cover-image {
  margin-bottom: 2rem;
  text-align: center; /* 图片居中 */
}
.article-cover-image img {
  max-width: 100%;
  height: auto;
  border-radius: 0.3rem; /* 轻微圆角 */
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.article-body {
  font-size: 1.05rem; /* 稍微增大正文字体 */
  line-height: 1.75; /* 增加行高 */
  color: #343a40; /* 深灰色 */
  word-wrap: break-word;
}
/* 确保 v-html 内容有基本样式 (从 App.vue 继承或在此处定义) */
.article-body :deep(p) { margin-bottom: 1.2em; }
.article-body :deep(h1),
.article-body :deep(h2),
.article-body :deep(h3),
.article-body :deep(h4) {
  margin-top: 1.8em;
  margin-bottom: 0.8em;
  line-height: 1.4;
  font-weight: 600;
  color: #2c3e50;
}
.article-body :deep(ul), .article-body :deep(ol) { padding-left: 1.8em; margin-bottom: 1.2em; }
.article-body :deep(blockquote) {
  margin: 1.5em 0;
  padding: 0.5em 1em 0.5em 1.5em;
  border-left: 4px solid #007bff; /* 主题色边框 */
  background-color: #f8f9fa; /* 浅背景 */
  color: #495057;
  font-style: italic;
}
.article-body :deep(pre), .article-body :deep(code-block) {
  background-color: #282c34; /* 暗色代码块背景 */
  color: #abb2bf; /* 浅色代码文字 */
  padding: 1em;
  border-radius: 0.3rem;
  overflow-x: auto;
  margin-bottom: 1.2em;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
  font-size: 0.9em;
}
.article-body :deep(img) {
    max-width: 100%;
    height: auto;
    border-radius: 0.3rem;
    margin: 1.5em auto; /* 图片上下外边距并居中 */
    display: block;
}
.article-body :deep(a) {
    color: #007bff;
    text-decoration: none;
}
.article-body :deep(a:hover) {
    text-decoration: underline;
}


.separator {
  margin: 2.5rem 0;
  border: 0;
  border-top: 1px solid #dee2e6; /* 更浅的分割线 */
}

/* loading, error, not-found 样式会从 App.vue 继承或在此处定义 */
.loading-indicator, .error-message, .not-found {
  padding: 2rem;
  text-align: center;
}
.not-found .button, .error-message .button {
    margin-top: 1rem;
}
</style>