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
  border-radius: 0.5rem; /* 更大的圆角 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); /* 更柔和且弥散的阴影 */
  overflow: hidden;
  /* margin-bottom: 20px; */ /* 由父容器的 gap 控制 */
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
  display: flex; /* 允许更灵活的内部布局 */
  flex-direction: column;
  height: 100%; /* 配合 grid 布局填满单元格 */
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.article-cover {
  width: 100%;
  height: 180px; /* 调整封面高度 */
  object-fit: cover;
  border-bottom: 1px solid #eee; /* 图片和内容间的细微分割 */
}

.article-content {
  padding: 1rem; /* 调整内边距 */
  display: flex;
  flex-direction: column;
  flex-grow: 1; /* 使内容区域填满剩余空间 */
}

.article-title {
  font-size: 1.25rem; /* 调整标题大小 */
  margin-top: 0;
  margin-bottom: 0.5rem; /* 减小与摘要的间距 */
  color: #212529; /* 更深的标题颜色 */
  font-weight: 600;
  line-height: 1.3;
  /* 多行文字溢出省略 (可选) */
  /* display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis; */
}

.article-excerpt {
  font-size: 0.9rem; /* 调整摘要字体 */
  color: #6c757d; /* 中性灰色 */
  margin-bottom: 1rem; /* 增大与元数据的间距 */
  line-height: 1.5;
  flex-grow: 1; /* 使摘要区域也参与空间分配 */
  /* 多行文字溢出省略 (可选) */
  /* display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis; */
}

.article-meta {
  font-size: 0.8rem; /* 调整元数据字体 */
  color: #868e96;
  display: flex;
  flex-wrap: wrap; /* 允许换行 */
  gap: 0.5rem 1rem; /* 行间距和项间距 */
  margin-top: auto; /* 将元数据推到底部 */
  padding-top: 0.5rem; /* 与上方内容间距 */
  border-top: 1px solid #f1f3f5; /* 元数据与摘要的细微分割 */
}

.article-meta span {
  margin-right: 0; /* 通过 gap 控制间距 */
  display: flex; /* 用于图标对齐（如果未来添加图标） */
  align-items: center;
}

.article-meta .category {
  background-color: #e0e7ff; /* 调整分类标签颜色 */
  color: #4338ca;
  padding: 0.15rem 0.4rem;
  border-radius: 0.2rem;
  font-weight: 500;
}
</style>