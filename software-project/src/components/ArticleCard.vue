<template>
  <div class="article-card" @click="navigateToDetail">
    <img v-if="article.cover_image" :src="article.cover_image" alt="Article Cover" class="article-cover">
    <div class="article-content">
      <h3 class="article-title">{{ article.title }}</h3>
      <p class="article-excerpt">{{ article.excerpt || truncate(article.content, 100) }}</p>
      <div class="article-meta">
        <span class="author">作者: {{ article.author?.username || '未知' }}</span>
        <span class="category" v-if="article.category_details">分类: {{ article.category_details?.name || '未分类' }}</span>
        <span class="date">发布于: {{ formatDate(article.created_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
});

const router = useRouter();

const navigateToDetail = () => {
  router.push({ name: 'ArticleDetail', params: { id: props.article.id } });
};

const truncate = (text, length) => {
  if (text && text.length > length) {
    return text.substring(0, length) + '...';
  }
  return text;
};

const formatDate = (dateString) => {
  if (!dateString) return '未知日期';
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};
</script>

<style scoped>
.article-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  overflow: hidden;
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}
.article-card:hover {
  transform: translateY(-5px);
}
.article-cover {
  width: 100%;
  height: 200px;
  object-fit: cover;
}
.article-content {
  padding: 15px;
}
.article-title {
  font-size: 1.4em;
  margin-top: 0;
  margin-bottom: 10px;
  color: #333;
}
.article-excerpt {
  font-size: 0.95em;
  color: #666;
  margin-bottom: 15px;
  line-height: 1.6;
}
.article-meta {
  font-size: 0.85em;
  color: #888;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.article-meta span {
  margin-right: 15px;
}
.article-meta .category {
  background-color: #e7f3ff;
  color: #007bff;
  padding: 2px 6px;
  border-radius: 4px;
}
</style>