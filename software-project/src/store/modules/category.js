// src/store/modules/category.js
import axios from 'axios';

const state = {
  categories: [], // 所有分类
  isLoading: false,
  error: null,
};

const getters = {
  allCategories: state => state.categories,
  categoryIsLoading: state => state.isLoading,
  categoryError: state => state.error,
};

const mutations = {
  SET_CATEGORIES(state, categories) {
    state.categories = categories;
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