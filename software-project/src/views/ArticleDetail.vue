<template>
  <div class="article-detail-page">
    <!-- ... existing template ... -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'; // 引入 onBeforeUnmount
import { useStore } from 'vuex';
import { useRoute, useRouter } from 'vue-router';
import CommentList from '@/components/CommentList.vue';

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
  // fetchArticleById action 内部已经有 SET_CURRENT_ARTICLE(null) 来清理
  store.dispatch('article/fetchArticleById', id).catch(err => {
    console.error("Failed to load article in component:", err);
  });
};

onMounted(() => {
  if (articleId.value) {
    fetchArticle(articleId.value);
  }
});

watch(() => route.params.id, (newId) => {
  if (newId && newId !== articleId.value) {
    articleId.value = newId;
    fetchArticle(newId);
  } else if (!newId && article.value) { // 如果从有 ID 的文章详情页导航到无 ID 的页面（不太可能，但作为健壮性考虑）
    store.commit('article/SET_CURRENT_ARTICLE', null);
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
    router.push('/home');
  } catch (err) {
    console.error('Failed to delete article:', err);
  } finally {
    isDeleting.value = false;
  }
};

// 组件卸载前，清空当前的具体文章数据，防止在快速切换或返回列表时短暂显示旧数据
onBeforeUnmount(() => {
  store.commit('article/SET_CURRENT_ARTICLE', null);
});
</script>

<style scoped>
/* ... existing styles ... */
</style>