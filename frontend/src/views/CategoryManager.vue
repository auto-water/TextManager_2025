<template>
  <div class="category-manager">
    <h2>分类管理</h2>

    <div v-if="isLoading" class="loading-indicator">加载分类中...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div class="category-form-section">
      <h3>{{ editingCategory ? '编辑分类' : '添加新分类' }}</h3>
      <form @submit.prevent="handleSaveCategory">
        <div class="form-group">
          <label for="category-name">分类名称:</label>
          <input type="text" id="category-name" v-model="currentCategory.name" required>
        </div>
        <div class="form-group">
          <label for="category-parent">父级分类 (可选, 用于二级/三级分类):</label>
          <select id="category-parent" v-model="currentCategory.parent">
            <option :value="null">无父级 (一级分类)</option>
            <!-- Populate with existing categories, excluding self if editing -->
            <template v-for="cat in availableParentCategories" :key="cat.id">
               <option :value="cat.id">{{ cat.name }}</option>
               <!-- Add options for children if you want to show hierarchy -->
            </template>
          </select>
        </div>
        <button type="submit" :disabled="isSubmitting">
          {{ isSubmitting ? '保存中...' : (editingCategory ? '更新分类' : '添加分类') }}
        </button>
        <button type="button" v-if="editingCategory" @click="cancelEdit" class="cancel-button">取消编辑</button>
      </form>
    </div>

    <div class="category-list-section">
      <h3>现有分类</h3>
      <ul v-if="categories.length > 0" class="category-tree">
        <!-- Render categories as a tree or flat list -->
        <!-- For simplicity, a flat list. A tree requires recursive component or more complex logic -->
        <li v-for="cat in sortedCategories" :key="cat.id" class="category-item">
          <span>
            {{ cat.name }}
            <small v-if="cat.parent_details"> (父: {{ cat.parent_details.name }})</small>
            <small v-else> (一级分类)</small>
          </span>
          <div class="category-actions">
            <button @click="editCategory(cat)" class="action-btn edit-btn">编辑</button>
            <button @click="deleteCategory(cat.id)" class="action-btn delete-btn" :disabled="isDeleting === cat.id">
               {{ isDeleting === cat.id ? '删除中...' : '删除' }}
            </button>
          </div>
        </li>
      </ul>
      <p v-else-if="!isLoading && !error">暂无分类。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

// Use the 'category' module if you created it.
// Otherwise, actions would be 'article/fetchCategories', 'article/createCategory' etc.
const CATEGORY_MODULE_NAMESPACE = 'category'; // Change to 'article' if categories are in article.js

const store = useStore();

const currentCategory = reactive({ name: '', parent: null });
const editingCategory = ref(null); // Store the category object being edited
const isSubmitting = ref(false);
const isDeleting = ref(null); // Store ID of category being deleted

// Use the correct module for getters
const categories = computed(() => store.getters[`${CATEGORY_MODULE_NAMESPACE}/allCategories`]);
const isLoading = computed(() => store.getters[`${CATEGORY_MODULE_NAMESPACE}/categoryIsLoading`]);
const error = computed(() => store.getters[`${CATEGORY_MODULE_NAMESPACE}/categoryError`]);

// To prevent selecting a category as its own parent or a child as its parent (complex for deep trees)
// For simplicity, allow any other category as parent.
const availableParentCategories = computed(() => {
  if (editingCategory.value) {
    return categories.value.filter(cat => cat.id !== editingCategory.value.id);
  }
  return categories.value;
});

// Fetch categories (and potentially their parent details) on mount
onMounted(() => {
  store.dispatch(`${CATEGORY_MODULE_NAMESPACE}/fetchCategories`);
});

const sortedCategories = computed(() => {
    // Simple sort by name for now. Could be hierarchical.
    return [...categories.value].sort((a,b) => a.name.localeCompare(b.name));
});


const handleSaveCategory = async () => {
  isSubmitting.value = true;
  store.commit(`${CATEGORY_MODULE_NAMESPACE}/CLEAR_ERROR`);
  try {
    const payload = {
      name: currentCategory.name,
      parent: currentCategory.parent // null if no parent
    };
    if (editingCategory.value) {
      await store.dispatch(`${CATEGORY_MODULE_NAMESPACE}/updateCategory`, { id: editingCategory.value.id, data: payload });
    } else {
      await store.dispatch(`${CATEGORY_MODULE_NAMESPACE}/createCategory`, payload);
    }
    resetForm();
    // Optionally: re-fetch categories to get the latest tree structure if parent details are important.
    // await store.dispatch(`${CATEGORY_MODULE_NAMESPACE}/fetchCategories`);
  } catch (err) {
    console.error('Failed to save category:', err);
  } finally {
    isSubmitting.value = false;
  }
};

const editCategory = (category) => {
  editingCategory.value = { ...category }; // Clone to avoid modifying original in list
  currentCategory.name = category.name;
  currentCategory.parent = category.parent; // This should be parent ID
};

const cancelEdit = () => {
  resetForm();
};

const resetForm = () => {
  editingCategory.value = null;
  currentCategory.name = '';
  currentCategory.parent = null;
};

const deleteCategory = async (categoryId) => {
  if (!confirm('确定要删除这个分类吗？其下的文章将变为未分类 (或按后端逻辑处理)。')) return;
  isDeleting.value = categoryId;
  store.commit(`${CATEGORY_MODULE_NAMESPACE}/CLEAR_ERROR`);
  try {
    await store.dispatch(`${CATEGORY_MODULE_NAMESPACE}/deleteCategory`, categoryId);
  } catch (err) {
    console.error('Failed to delete category:', err);
  } finally {
    isDeleting.value = null;
  }
};

// Helper to display parent name if your serializer provides nested parent details
// This depends on your CategorySerializer having `parent_details = CategorySerializer(source='parent', read_only=True)`
// Or you fetch them separately.
// For a simple parent ID, you might need to find the parent name from the categories list.
</script>

<style scoped>
.category-manager {
  max-width: 700px;
  margin: 20px auto;
  padding: 20px;
}
.category-manager h2, .category-manager h3 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}
.category-form-section, .category-list-section {
  background-color: #fff;
  padding: 25px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.07);
  margin-bottom: 30px;
}
.form-group {
  margin-bottom: 15px;
}
.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}
.category-manager button {
  margin-right: 10px;
}
.cancel-button {
    background-color: #6c757d;
}
.category-tree {
  list-style: none;
  padding-left: 0;
}
.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #eee;
}
.category-item:last-child {
  border-bottom: none;
}
.category-item small {
    color: #777;
    font-size: 0.85em;
}
.category-actions {
  display: flex;
  gap: 8px;
}
.action-btn {
    padding: 5px 10px;
    font-size: 0.9em;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
.edit-btn {
    background-color: #ffc107; /* Yellow for edit */
    color: #212529;
}
.delete-btn {
    background-color: #dc3545; /* Red for delete */
    color: white;
}
.action-btn:disabled {
    background-color: #ccc;
}
</style>