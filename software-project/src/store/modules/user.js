// src/store/modules/user.js
import axios from 'axios';

const state = {
  token: localStorage.getItem('user_token') || null,
  currentUser: JSON.parse(localStorage.getItem('current_user')) || null,
  users: [], // 用于管理员管理用户列表
  isLoading: false, // 新增：用于获取用户列表的加载状态
  error: null,
};

const getters = {
  isAuthenticated: state => !!state.token,
  currentUser: state => state.currentUser,
  isAdmin: state => state.currentUser && state.currentUser.is_staff,
  allUsers: state => state.users,
  isUserListLoading: state => state.isLoading, // 新增 getter
  authError: state => state.error
};

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token;
    localStorage.setItem('user_token', token);
  },
  SET_CURRENT_USER(state, user) {
    state.currentUser = user;
    localStorage.setItem('current_user', JSON.stringify(user));
  },
  SET_USERS(state, users) {
    state.users = users;
  },
  SET_USER_LIST_LOADING(state, isLoading) { // 新增 mutation
    state.isLoading = isLoading;
  },
  LOGOUT(state) {
    state.token = null;
    state.currentUser = null;
    localStorage.removeItem('user_token');
    localStorage.removeItem('current_user');
  },
  SET_ERROR(state, error) {
    state.error = error;
  },
  CLEAR_ERROR(state) {
    state.error = null;
  }
};

const actions = {
  async registerUser({ commit }, userData) {
    commit('CLEAR_ERROR');
    try {
      const response = await axios.post('/users/', userData);
      console.log('Registration successful', response.data);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.response?.data || error.message || 'Registration failed';
      commit('SET_ERROR', errorMessage);
      throw new Error(errorMessage);
    }
  },
  async loginUser({ commit, dispatch }, credentials) {
    commit('CLEAR_ERROR');
    try {
      const response = await axios.post('/auth/token/', credentials);
      const token = response.data.token;
      commit('SET_TOKEN', token);
      await dispatch('fetchCurrentUser');
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.response?.data || 'Login failed';
      commit('SET_ERROR', errorMessage);
      throw new Error(errorMessage);
    }
  },
  async fetchCurrentUser({ commit, state }) {
    if (!state.token) return;
    commit('CLEAR_ERROR');
    try {
      const response = await axios.get('/users/me/');
      commit('SET_CURRENT_USER', response.data);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch current user:', error);
      commit('LOGOUT');
      const errorMessage = error.response?.data?.detail || 'Failed to fetch user data';
      commit('SET_ERROR', errorMessage);
    }
  },
  logoutUser({ commit }) {
    commit('LOGOUT');
    // await axios.post('/auth/logout/'); // 可选
  },

  // --- Admin User Management Actions ---
  async fetchAllUsers({ commit }) {
    commit('SET_USER_LIST_LOADING', true); // 使用新增的状态
    commit('CLEAR_ERROR');
    try {
      const response = await axios.get('/users/');
      commit('SET_USERS', response.data.results || response.data); // 假设后端分页或直接返回列表
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to fetch users';
      commit('SET_ERROR', errorMessage);
      throw new Error(errorMessage);
    } finally {
      commit('SET_USER_LIST_LOADING', false); // 使用新增的状态
    }
  },
  async updateUserAdmin({ commit, dispatch }, { userId, data }) {
    commit('CLEAR_ERROR');
    try {
      const response = await axios.put(`/users/${userId}/`, data);
      // 为了确保数据一致性，可以重新获取特定用户或整个列表
      // 这里选择重新获取整个列表，或者也可以只更新本地 `state.users` 中的对应项
      dispatch('fetchAllUsers'); // 简单处理，重新获取列表
      console.log('User updated by admin', response.data);
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to update user';
      commit('SET_ERROR', errorMessage);
      throw new Error(errorMessage);
    }
  },
   async deleteUserAdmin({ commit, dispatch }, userId) {
    commit('CLEAR_ERROR');
    try {
      await axios.delete(`/users/${userId}/`);
      dispatch('fetchAllUsers'); // 删除后重新获取列表
      console.log(`User ${userId} deleted by admin`);
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Failed to delete user';
      commit('SET_ERROR', errorMessage);
      throw new Error(errorMessage);
    }
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};