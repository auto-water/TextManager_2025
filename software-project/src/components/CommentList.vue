<template>
  <div class="comment-section">
    <h4>评论 ({{ comments.length }})</h4>
    <div v-if="isLoading" class="loading-indicator">加载评论中...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <form @submit.prevent="submitComment" class="comment-form" v-if="isAuthenticated">
      <textarea v-model="newCommentContent" placeholder="发表你的看法..." required></textarea>
      <button type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? '提交中...' : '发表评论' }}
      </button>
    </form>
    <p v-else>请 <router-link :to="{ name: 'Login', query: { redirect: $route.fullPath }}">登录</router-link> 后发表评论。</p>


    <ul v-if="comments.length > 0" class="comment-list">
      <li v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-author">
          <strong>{{ comment.author?.username || '匿名用户' }}</strong>
          <span class="comment-date">{{ formatDate(comment.created_at) }}</span>
        </div>
        <p class="comment-content">{{ comment.content }}</p>
        <button
          v-if="canDeleteComment(comment)"
          @click="deleteComment(comment.id)"
          class="delete-comment-button"
          :disabled="isDeleting === comment.id"
        >
          {{ isDeleting === comment.id ? '删除中...' : '删除' }}
        </button>
      </li>
    </ul>
    <p v-else-if="!isLoading && !error">还没有评论。</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios'; // Or use a dedicated API service
import { useStore } from 'vuex';
import { useRoute } from 'vue-router';

const props = defineProps({
  articleId: {
    type: [String, Number],
    required: true
  }
});

const store = useStore();
const route = useRoute(); // For login redirect

const comments = ref([]);
const newCommentContent = ref('');
const isLoading = ref(false);
const isSubmitting = ref(false);
const isDeleting = ref(null); // Store ID of comment being deleted
const error = ref(null);

const isAuthenticated = computed(() => store.getters['user/isAuthenticated']);
const currentUser = computed(() => store.getters['user/currentUser']);
const isAdmin = computed(() => store.getters['user/isAdmin']);

const fetchComments = async () => {
  if (!props.articleId) return;
  isLoading.value = true;
  error.value = null;
  try {
    const response = await axios.get(`/comments/`, { params: { article: props.articleId } });
    // DRF ViewSet list action for comments usually filters by article_id query param
    // and returns a list (or paginated response)
    comments.value = response.data.results || response.data; // Adjust based on API response
  } catch (err) {
    console.error('Failed to fetch comments:', err);
    error.value = '无法加载评论。';
  } finally {
    isLoading.value = false;
  }
};

const submitComment = async () => {
  if (!newCommentContent.value.trim()) return;
  isSubmitting.value = true;
  error.value = null;
  try {
    const response = await axios.post('/comments/', {
      article: props.articleId,
      content: newCommentContent.value
    });
    comments.value.unshift(response.data); // Add to the top
    newCommentContent.value = '';
  } catch (err) {
    console.error('Failed to post comment:', err);
    error.value = '评论发表失败。';
  } finally {
    isSubmitting.value = false;
  }
};

const deleteComment = async (commentId) => {
  if (!confirm('确定要删除这条评论吗？')) return;
  isDeleting.value = commentId;
  error.value = null;
  try {
    await axios.delete(`/comments/${commentId}/`);
    comments.value = comments.value.filter(c => c.id !== commentId);
  } catch (err) {
    console.error('Failed to delete comment:', err);
    error.value = '删除评论失败。';
  } finally {
    isDeleting.value = null;
  }
};

const canDeleteComment = (comment) => {
  if (!currentUser.value) return false;
  return isAdmin.value || comment.author?.id === currentUser.value.id;
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleString();
};

onMounted(() => {
  fetchComments();
});

// Watch for articleId changes if this component might be reused on the same page for different articles
watch(() => props.articleId, (newId, oldId) => {
  if (newId && newId !== oldId) {
    fetchComments();
  }
});

</script>

<style scoped>
.comment-section {
  margin-top: 30px;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}
.comment-section h4 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
}
.comment-form textarea {
  width: 100%;
  min-height: 80px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
  box-sizing: border-box;
}
.comment-form button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
}
.comment-form button:disabled {
  background-color: #aaa;
}
.comment-list {
  list-style-type: none;
  padding: 0;
}
.comment-item {
  background-color: #fff;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 10px;
}
.comment-author {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
  font-size: 0.9em;
}
.comment-author strong {
  color: #007bff;
}
.comment-date {
  color: #777;
  font-size: 0.85em;
}
.comment-content {
  color: #555;
  line-height: 1.6;
  white-space: pre-wrap; /* Preserve line breaks */
}
.delete-comment-button {
  background-color: transparent;
  color: #dc3545;
  border: none;
  padding: 5px 0;
  font-size: 0.85em;
  cursor: pointer;
  margin-top: 5px;
}
.delete-comment-button:hover {
  text-decoration: underline;
}
.delete-comment-button:disabled {
  color: #aaa;
}
</style>