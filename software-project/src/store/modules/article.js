// src/store/modules/article.js
import axios from 'axios';

const state = {
  articles: [],
  currentArticle: null,
  categories: [],
  isLoading: false,
  error: null,
  pagination: {
    count: 0,
    next: null,
    previous: null,
    currentPage: 1,
    totalPages: 1,
    pageSize: 10
  }
};

const getters = {
  allArticles: state => state.articles,
  currentArticleDetail: state => state.currentArticle,
  allCategories: state => state.categories,
  articleIsLoading: state => state.isLoading,
  articleError: state => state.error,
  articlePagination: state => state.pagination,
};

const mutations = {
  SET_LOADING(state, isLoading) {
    state.isLoading = isLoading;
  },
  SET_ERROR(state, error) {
    state.error = error;
  },
  CLEAR_ERROR(state) {
    state.error = null;
  },
  SET_ARTICLES(state, { results, count, next, previous }) {
    state.articles = results;
    state.pagination.count = count;
    state.pagination.next = next;
    state.pagination.previous = previous;
    state.pagination.totalPages = Math.ceil(count / state.pagination.pageSize);
  },
  SET_CURRENT_ARTICLE(state, article) {
    state.currentArticle = article;
  },
  ADD_ARTICLE(state, article) {
    state.articles.unshift(article);
  },
  UPDATE_ARTICLE_IN_LIST(state, updatedArticle) {
    const index = state.articles.findIndex(a => a.id === updatedArticle.id);
    if (index !== -1) {
      state.articles.splice(index, 1, updatedArticle);
    }
    // 如果更新的是当前文章，也更新 currentArticle
    if (state.currentArticle && state.currentArticle.id === updatedArticle.id) {
        state.currentArticle = { ...state.currentArticle, ...updatedArticle };
    }
  },
  REMOVE_ARTICLE_FROM_LIST(state, articleId) {
    state.articles = state.articles.filter(a => a.id !== articleId);
  },
  SET_CATEGORIES(state, categories) {
    state.categories = categories;
  },
  SET_CURRENT_PAGE(state, page) {
    state.pagination.currentPage = page;
  }
};

const actions = {
  async fetchArticles({ commit, state }, { search = '', category = '', status = 'published', page = 1 } = {}) {
    commit('SET_LOADING', true);
    commit('CLEAR_ERROR');
    try {
      const params = { search, status, page, page_size: state.pagination.pageSize };
      if (category) params.category = category;

      const response = await axios.get('/articles/', { params });
      commit('SET_ARTICLES', response.data);
      commit('SET_CURRENT_PAGE', page);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to fetch articles';
      commit('SET_ERROR', errorMessage);
      throw new Error(errorMessage);
    } finally {
      commit('SET_LOADING', false);
    }
  },
  async fetchArticleById({ commit }, articleId) {
    commit('SET_LOADING', true);
    commit('CLEAR_ERROR');
    commit('SET_CURRENT_ARTICLE', null); // 在获取新文章前清空，避免短暂显示旧数据
    try {
      const response = await axios.get(`/articles/${articleId}/`);
      commit('SET_CURRENT_ARTICLE', response.data);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to fetch article';
      commit('SET_ERROR', errorMessage);
      throw new Error(errorMessage);
    } finally {
      commit('SET_LOADING', false);
    }
  },
  async createArticle({ commit }, articleData) {
    commit('SET_LOADING', true);
    commit('CLEAR_ERROR');
    try {
      const response = await axios.post('/articles/', articleData);
      // commit('ADD_ARTICLE', response.data); // 可选立即更新列表
      // 更好的做法是，如果创建后跳转到详情页，则不需要立即更新列表
      // 如果创建后停留在列表页，则需要更新
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.response?.data || 'Failed to create article';
      commit('SET_ERROR', errorMessage);
      throw new Error(errorMessage);
    } finally {
      commit('SET_LOADING', false);
    }
  },
  async updateArticle({ commit }, { articleId, articleData }) {
    commit('SET_LOADING', true);
    commit('CLEAR_ERROR');
    try {
      const response = await axios.put(`/articles/${articleId}/`, articleData);
      commit('UPDATE_ARTICLE_IN_LIST', response.data);
      // 如果当前详情页正是这个文章，也更新它
      if (state.currentArticle && state.currentArticle.id === articleId) {
        commit('SET_CURRENT_ARTICLE', response.data);
      }
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.response?.data || 'Failed to update article';
      commit('SET_ERROR', errorMessage);
      throw new Error(errorMessage);
    } finally {
      commit('SET_LOADING', false);
    }
  },
  async deleteArticle({ commit }, articleId) {
    commit('SET_LOADING', true);
    commit('CLEAR_ERROR');
    try {
      await axios.delete(`/articles/${articleId}/`);
      commit('REMOVE_ARTICLE_FROM_LIST', articleId);
      if (state.currentArticle && state.currentArticle.id === articleId) {
        commit('SET_CURRENT_ARTICLE', null);
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to delete article';
      commit('SET_ERROR', errorMessage);
      throw new Error(errorMessage);
    } finally {
      commit('SET_LOADING', false);
    }
  },
  async fetchCategories({ commit }) {
    commit('CLEAR_ERROR'); // 假设分类有单独的错误状态或共享文章错误状态
    try {
      const response = await axios.get('/categories/');
      commit('SET_CATEGORIES', response.data.results || response.data);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to fetch categories';
      commit('SET_ERROR', errorMessage);
      throw new Error(errorMessage);
    }
  },
  // 移除了 fetchCommentsForArticle 和 postComment actions
  // 因为 CommentList.vue 已经自行处理
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};