// src/store/modules/category.js (或 article.js)
import axios from 'axios';

const state = {
  categories: [], // 原始扁平分类列表
  isLoading: false,
  error: null,
};

const getters = {
  allCategoriesRaw: state => state.categories, // 返回原始扁平列表
  // 新增 getter：将扁平列表转换为适合 <select> 的带层级前缀的列表
  categoriesForSelect: state => {
    const categories = state.categories;
    if (!categories || categories.length === 0) {
      return [];
    }

    const categoryMap = {};
    const tree = [];
    const resultForSelect = [];

    // 1. 构建 Map 和顶级节点
    categories.forEach(cat => {
      categoryMap[cat.id] = { ...cat, children: [] }; // 复制并添加 children 数组
    });

    // 2. 构建树形结构
    categories.forEach(cat => {
      const mappedCat = categoryMap[cat.id];
      if (cat.parent && categoryMap[cat.parent]) { // cat.parent 是父ID
        categoryMap[cat.parent].children.push(mappedCat);
      } else {
        tree.push(mappedCat); // 顶级节点
      }
    });

    // 3. 递归遍历树，生成带前缀的列表项
    function buildSelectOptions(nodes, depth = 0) {
      for (const node of nodes) {
        let prefix = '';
        for (let i = 0; i < depth; i++) {
          prefix += '  '; // 使用两个空格作为一级缩进
        }
        if (depth > 0) {
            prefix += '└─ ';
        }

        resultForSelect.push({
          id: node.id,
          name: prefix + node.name, // 添加前缀
          originalName: node.name, // 保留原始名称（如果需要）
          depth: depth, // 保留深度（如果需要）
        });
        if (node.children && node.children.length > 0) {
          // 对子节点排序 (可选, 按名称)
          node.children.sort((a, b) => a.name.localeCompare(b.name));
          buildSelectOptions(node.children, depth + 1);
        }
      }
    }
    // 对顶级节点排序 (可选, 按名称)
    tree.sort((a,b) => a.name.localeCompare(b.name));
    buildSelectOptions(tree);
    return resultForSelect;
  },
  categoryIsLoading: state => state.isLoading,
  categoryError: state => state.error,
};

const mutations = {
  SET_CATEGORIES(state, categories) {
    // 确保 categories 是数组
    state.categories = Array.isArray(categories) ? categories : [];
  },
  ADD_CATEGORY(state, category) {
    state.categories.push(category);
  },
  UPDATE_CATEGORY(state, updatedCategory) {
    const index = state.categories.findIndex(c => c.id === updatedCategory.id);
    if (index !== -1) {
      state.categories.splice(index, 1, updatedCategory);
    }
  },
  REMOVE_CATEGORY(state, categoryId) {
    state.categories = state.categories.filter(c => c.id !== categoryId);
  },
  SET_LOADING(state, isLoading) {
    state.isLoading = isLoading;
  },
  SET_ERROR(state, error) {
    state.error = error;
  },
  CLEAR_ERROR(state) {
    state.error = null;
  }
};

const actions = {
  async fetchCategories({ commit }) {
    commit('SET_LOADING', true);
    commit('CLEAR_ERROR');
    try {
      const response = await axios.get('/categories/');
      commit('SET_CATEGORIES', response.data.results || response.data);
      return response.data;
    } catch (err) {
      commit('SET_ERROR', err.response?.data?.detail || 'Failed to fetch categories');
      throw err;
    } finally {
      commit('SET_LOADING', false);
    }
  },
  async createCategory({ commit }, categoryData) {
    commit('SET_LOADING', true);
    commit('CLEAR_ERROR');
    try {
      const response = await axios.post('/categories/', categoryData);
      commit('ADD_CATEGORY', response.data);
      return response.data;
    } catch (err) {
      commit('SET_ERROR', err.response?.data?.detail || 'Failed to create category');
      throw err;
    } finally {
      commit('SET_LOADING', false);
    }
  },
  async updateCategory({ commit }, { id, data }) {
    commit('SET_LOADING', true);
    commit('CLEAR_ERROR');
    try {
      const response = await axios.put(`/categories/${id}/`, data);
      commit('UPDATE_CATEGORY', response.data);
      return response.data;
    } catch (err) {
      commit('SET_ERROR', err.response?.data?.detail || 'Failed to update category');
      throw err;
    } finally {
      commit('SET_LOADING', false);
    }
  },
  async deleteCategory({ commit }, categoryId) {
    commit('SET_LOADING', true);
    commit('CLEAR_ERROR');
    try {
      await axios.delete(`/categories/${categoryId}/`);
      commit('REMOVE_CATEGORY', categoryId);
    } catch (err) {
      commit('SET_ERROR', err.response?.data?.detail || 'Failed to delete category');
      throw err;
    } finally {
      commit('SET_LOADING', false);
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};