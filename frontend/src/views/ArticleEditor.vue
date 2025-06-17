<template>
  <div class="editor-page">
    <h2>{{ editingArticleId ? '编辑文章' : '撰写新文章' }}</h2>
    <form @submit.prevent="handlePublish">
      <div class="form-group">
        <label for="title">文章标题</label>
        <input id="title" v-model="article.title" placeholder="文章标题" required />
      </div>

      <div class="form-group">
        <label for="category">选择分类</label>
        <select id="category" v-model="article.category" required>
          <option disabled value="">请选择一个分类</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
      </div>
      
      <div class="form-group">
        <label>文章内容</label>
        <RichTextEditor v-model="article.content" />
         <!-- Fallback if RichTextEditor is problematic during setup -->
         <!-- <textarea v-model="article.content" rows="10" placeholder="文章内容..."></textarea> -->
      </div>
      
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>


      <div class="actions">
        <button type="button" @click="handleSaveAsDraft" :disabled="isLoading" class="draft-button">
          {{ isLoading && currentAction === 'draft' ? '保存中...' : '保存草稿' }}
        </button>
        <button type="submit" :disabled="isLoading" class="publish-button">
          {{ isLoading && currentAction === 'publish' ? '发布中...' : '发布文章' }}
        </button>
         <button type="button" @click="goBack" class="cancel-button">取消</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter, useRoute } from 'vue-router';
import RichTextEditor from '@/components/RichTextEditor.vue';

const store = useStore();
const router = useRouter();
const route = useRoute();

const article = reactive({
  title: '',
  content: '',
  category: null, // Store category ID
  status: 'draft' // Default status
});
const editingArticleId = ref(route.params.id || null); // Get ID from route params
const isLoading = ref(false);
const currentAction = ref(''); // 'draft' or 'publish'
const successMessage = ref('');

const categories = computed(() => store.getters['article/allCategories']);
const error = computed(() => store.getters['article/articleError']);

const loadArticleForEditing = async (id) => {
  isLoading.value = true;
  try {
    // Fetch the full article details, not just from the list in store
    // because the list might have excerpts.
    const existingArticle = await store.dispatch('article/fetchArticleById', id);
    if (existingArticle) {
      article.title = existingArticle.title;
      article.content = existingArticle.content;
      article.category = existingArticle.category; // Assumes category is ID
      article.status = existingArticle.status;
    } else {
      // Article not found, redirect or show error
      router.push('/home'); // Or a 404 page
    }
  } catch (err) {
    console.error('Failed to load article for editing:', err);
    router.push('/home');
  } finally {
    isLoading.value = false;
  }
};

onMounted(async () => {
  store.dispatch('article/fetchCategories'); // Load categories for the dropdown
  if (editingArticleId.value) {
    await loadArticleForEditing(editingArticleId.value);
  }
});

// Watch for route param changes if navigating between editors
watch(() => route.params.id, (newId) => {
  editingArticleId.value = newId || null;
  if (newId) {
    loadArticleForEditing(newId);
  } else {
    // Reset form for new article
    Object.assign(article, { title: '', content: '', category: null, status: 'draft' });
  }
});

const saveArticle = async (status) => {
  isLoading.value = true;
  currentAction.value = status;
  successMessage.value = '';
  store.commit('article/CLEAR_ERROR');

  const articleData = {
    title: article.title,
    content: article.content,
    category: article.category,
    status: status
  };

  try {
    let savedArticle;
    if (editingArticleId.value) {
      savedArticle = await store.dispatch('article/updateArticle', {
        articleId: editingArticleId.value,
        articleData
      });
      successMessage.value = '文章更新成功！';
    } else {
      savedArticle = await store.dispatch('article/createArticle', articleData);
      successMessage.value = '文章创建成功！';
      // After creating, update editingArticleId for subsequent saves/publishes on this page
      // editingArticleId.value = savedArticle.id; // Or redirect
    }

    // Redirect based on status
    if (status === 'published') {
      router.push({ name: 'ArticleDetail', params: { id: savedArticle.id } });
    } else { // draft
      router.push('/drafts');
    }

  } catch (err) {
    console.error(`Failed to ${editingArticleId.value ? 'update' : 'create'} article:`, err);
    // Error is set in Vuex, will be displayed by computed 'error'
  } finally {
    isLoading.value = false;
    currentAction.value = '';
  }
};

const handleSaveAsDraft = () => {
  saveArticle('draft');
};

const handlePublish = () => {
  saveArticle('published');
};

const goBack = () => {
  router.back();
};
</script>

<style scoped>
.editor-page {
  max-width: 800px;
  margin: 20px auto;
  padding: 25px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.editor-page h2 {
  text-align: center;
  margin-bottom: 25px;
  color: #333;
}
.form-group {
  margin-bottom: 20px;
}
.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #444;
}
/* 表单元素样式：使用白色背景 */
.form-group input,
.form-group select {
  width: 100%;
  box-sizing: border-box;
  padding: 12px 14px;
  font-size: 1.08rem;
  border: 1px solid #ced4da; /* 更柔和的灰色边框 */
  border-radius: 7px;
  background: #ffffff; /* 纯白色背景 */
  transition: border 0.2s, box-shadow 0.2s;
  outline: none;
}
.form-group input:focus,
.form-group select:focus {
  border-color: #80bdff; /* 聚焦时的边框颜色 */
  box-shadow: 0 2px 8px rgba(0,123,255,0.08);
}
.actions {
  margin-top: 30px;
  display: flex;
  justify-content: flex-end; /* Align buttons to the right */
  gap: 10px;
}

.actions button {
  padding: 10px 20px;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

/* 取消按钮样式 */
.cancel-button {
  background-color: #f8f9fa; /* 浅灰色背景 */
  border: 1px solid #ced4da;
  color: #6c757d; /* 中灰色字体 */
}

.cancel-button:hover {
  background-color: #e9ecef;
  color: #495057; /* 悬停时加深颜色 */
}

/* 保存草稿按钮样式 */
.draft-button {
  background-color: #e9ecef; /* 浅灰色背景 */
  border: 1px solid #ced4da;
  color: #495057; /* 深灰色字体 */
}

.draft-button:hover {
  background-color: #dee2e6;
  color: #212529; /* 悬停时加深颜色 */
}

/* 发布文章按钮样式 */
.publish-button {
  background-color: #007bff; /* 蓝色背景 */
  border: 1px solid #0069d9;
  color: white;
}

.publish-button:hover {
  background-color: #0069d9;
}

/* 禁用状态 */
.actions button:disabled {
  background-color: #e9ecef;
  border-color: #ced4da;
  color: #adb5bd;
  cursor: not-allowed;
  opacity: 0.7;
}
.success-message {
  color: green;
  background-color: #e6ffed;
  border: 1px solid #b7ebc0;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 15px;
  text-align: center;
}
/* RichTextEditor might need specific styling for its container if not handled internally */
</style>