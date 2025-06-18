<template>
  <div class="category-manager">
    <h2>分类管理</h2>
    <!-- ... (loading, error messages) ... -->

    <div class="category-form-section">
      <h3>{{ editingCategory ? '编辑分类' : '添加新分类' }}</h3>
      <form @submit.prevent="handleSaveCategory">
        <div class="form-group">
          <label for="category-name">分类名称:</label>
          <input type="text" id="category-name" v-model="currentCategoryForm.name" required>
        </div>

        <div class="form-group">
          <label>选择父级分类 (可选):</label>
          <!-- 一级父分类选择 -->
          <select v-model="selectedParentLevel1" @change="onParentLevel1Change" class="category-select">
            <option :value="null">无父级 (设为一级分类)</option>
            <option v-for="catL1 in availableLevel1Parents" :key="catL1.id" :value="catL1.id">
              {{ catL1.name }}
            </option>
          </select>

          <!-- 二级父分类选择 (如果一级父分类被选中，且它有子分类可作为二级父分类) -->
          <select v-if="selectedParentLevel1 && availableLevel2Parents.length > 0" v-model="selectedParentLevel2" @change="onParentLevel2Change" class="category-select">
            <option :value="null">不选择二级父级 (父级为选定的一级)</option>
            <option v-for="catL2 in availableLevel2Parents" :key="catL2.id" :value="catL2.id">
              {{ catL2.name }}
            </option>
          </select>
          <!-- 注意：理论上还可以有三级父分类选择，但一个分类只有一个直接父级。
               这里的逻辑是让用户选择一个已存在的分类作为其父级。
               如果允许创建三级分类，用户需要选择一个二级分类作为其父级。
          -->
        </div>

        <button type="submit" :disabled="isSubmitting">
          {{ isSubmitting ? '保存中...' : (editingCategory ? '更新分类' : '添加分类') }}
        </button>
        <button type="button" v-if="editingCategory" @click="cancelEdit" class="cancel-button">取消编辑</button>
      </form>
    </div>

    <div class="category-list-section">
      <h3>现有分类 (使用带层级的列表)</h3>
      <ul v-if="formattedCategoriesForDisplay.length > 0" class="category-tree">
        <li v-for="cat in formattedCategoriesForDisplay" :key="cat.id" class="category-item">
          <span>{{ cat.name }}</span> <!-- name 已经包含了缩进 -->
          <div class="category-actions">
            <button @click="deleteCategory(cat.id)" class="action-btn delete-btn" :disabled="isDeleting === cat.id">
               {{ isDeleting === cat.id ? '删除中...' : '删除' }}
            </button>
          </div>
        </li>
      </ul>
      <!-- ... (no categories message) ... -->
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { useStore } from 'vuex';

const CATEGORY_MODULE_NAMESPACE = 'category'; // Or 'article' if categories are there
const store = useStore();

// 用于表单的响应式对象
const currentCategoryForm = reactive({ name: '', parent: null });
const editingCategory = ref(null); // 存储正在编辑的原始分类对象
const isSubmitting = ref(false);
const isDeleting = ref(null);

// 用于父级分类联动选择的状态
const selectedParentLevel1 = ref(null);
const selectedParentLevel2 = ref(null);

const allRawCategories = computed(() => store.getters[`${CATEGORY_MODULE_NAMESPACE}/allCategoriesRaw`]);
const isLoading = computed(() => store.getters[`${CATEGORY_MODULE_NAMESPACE}/categoryIsLoading`]);
const error = computed(() => store.getters[`${CATEGORY_MODULE_NAMESPACE}/categoryError`]);

// 用于在列表中展示带层级缩进的分类 (复用 category.js 中的 getter)
const formattedCategoriesForDisplay = computed(() => store.getters[`${CATEGORY_MODULE_NAMESPACE}/categoriesForSelect`]);


// 计算可选的一级父分类 (所有顶级分类)
const availableLevel1Parents = computed(() => {
  let categories = allRawCategories.value;
  if (editingCategory.value) { // 编辑时，不能选自己或自己的子孙作为父级 (简化：先只排除自己)
    categories = categories.filter(c => c.id !== editingCategory.value.id);
  }
  return categories.filter(cat => !cat.parent);
});

// 计算可选的二级父分类 (选定的一级父分类的直接子级)
const availableLevel2Parents = computed(() => {
  if (!selectedParentLevel1.value) return [];
  let categories = allRawCategories.value;
   if (editingCategory.value) { // 编辑时，不能选自己或自己的子孙作为父级 (简化：先只排除自己)
    categories = categories.filter(c => c.id !== editingCategory.value.id);
  }
  return categories.filter(cat => cat.parent === selectedParentLevel1.value);
});

const onParentLevel1Change = () => {
  selectedParentLevel2.value = null; // 重置二级父分类选择
  // 更新 currentCategoryForm.parent
  currentCategoryForm.parent = selectedParentLevel1.value;
};

const onParentLevel2Change = () => {
  // 更新 currentCategoryForm.parent
  // 如果选了二级父分类，则它成为真正的父级；否则父级是一级选中的
  currentCategoryForm.parent = selectedParentLevel2.value || selectedParentLevel1.value;
};


onMounted(() => {
  store.dispatch(`${CATEGORY_MODULE_NAMESPACE}/fetchCategories`);
});

const handleSaveCategory = async () => {
  isSubmitting.value = true;
  store.commit(`${CATEGORY_MODULE_NAMESPACE}/CLEAR_ERROR`);
  try {
    // 确定最终的父级ID
    let finalParentId = null;
    if (selectedParentLevel2.value) {
      finalParentId = selectedParentLevel2.value;
    } else if (selectedParentLevel1.value) {
      finalParentId = selectedParentLevel1.value;
    }
    // 如果表单中直接绑定了 currentCategoryForm.parent，确保它在联动时被正确更新
    // 或者直接在这里组合：
    const payload = {
      name: currentCategoryForm.name,
      parent: finalParentId // 使用最终确定的父级ID
    };

    if (editingCategory.value) {
      await store.dispatch(`${CATEGORY_MODULE_NAMESPACE}/updateCategory`, { id: editingCategory.value.id, data: payload });
    } else {
      await store.dispatch(`${CATEGORY_MODULE_NAMESPACE}/createCategory`, payload);
    }
    resetForm();
    store.dispatch(`${CATEGORY_MODULE_NAMESPACE}/fetchCategories`); // 重新获取以刷新列表和选项
  } catch (err) {
    console.error('Failed to save category:', err);
  } finally {
    isSubmitting.value = false;
  }
};

const editCategory = (categoryToEdit) => {
  editingCategory.value = { ...categoryToEdit }; // 存储原始对象
  currentCategoryForm.name = categoryToEdit.name;

  // 回填父级分类选择
  if (categoryToEdit.parent) {
    const parentCategory = allRawCategories.value.find(c => c.id === categoryToEdit.parent);
    if (parentCategory) {
      if (!parentCategory.parent) { // 父分类是一级分类
        selectedParentLevel1.value = parentCategory.id;
        selectedParentLevel2.value = null;
      } else { // 父分类是二级分类 (意味着当前编辑的是三级分类)
        const grandParentCategory = allRawCategories.value.find(c => c.id === parentCategory.parent);
        if (grandParentCategory) {
          selectedParentLevel1.value = grandParentCategory.id;
          selectedParentLevel2.value = parentCategory.id;
        } else { // 数据可能不一致或父级的父级未找到
          selectedParentLevel1.value = null;
          selectedParentLevel2.value = null;
        }
      }
    }
    currentCategoryForm.parent = categoryToEdit.parent; // 确保表单的 parent 也被设置
  } else { // 是一级分类
    selectedParentLevel1.value = null;
    selectedParentLevel2.value = null;
    currentCategoryForm.parent = null;
  }
};


const cancelEdit = () => {
  resetForm();
};

const resetForm = () => {
  editingCategory.value = null;
  currentCategoryForm.name = '';
  currentCategoryForm.parent = null;
  selectedParentLevel1.value = null;
  selectedParentLevel2.value = null;
};

const deleteCategory = async (categoryId) => {
  // ... (删除逻辑不变) ...
  if (!confirm('确定要删除这个分类吗？（警告：其下的文章将直接删除）')) return;
  isDeleting.value = categoryId;
  store.commit(`${CATEGORY_MODULE_NAMESPACE}/CLEAR_ERROR`);
  try {
    await store.dispatch(`${CATEGORY_MODULE_NAMESPACE}/deleteCategory`, categoryId);
    store.dispatch(`${CATEGORY_MODULE_NAMESPACE}/fetchCategories`); // 重新获取
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
  justify-content: flex-end; /* 确保单个按钮右对齐 */
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
.category-select { /* 给联动下拉框一些样式 */
  display: block;
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 0.5rem; /* 下拉框之间的间距 */
  border: 1px solid #ccc;
  border-radius: 4px;
}
.category-list-section .category-item span {
    white-space: pre; /* 保留缩进的空格 */
}
</style>