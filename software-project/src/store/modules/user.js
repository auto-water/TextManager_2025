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
      const response = await axios.post('/accounts/register/', userData); 
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
    // 原来的请求 (可能源于文档示例或之前的配置):
    // const response = await axios.post('/auth/token/', credentials);
    // 修改后的请求 (匹配后端 `backend_project/urls.py` 中的配置):
    const response = await axios.post('/token/', credentials); // 使用新的正确路径
    const token = response.data.token; // simplejwt 通常返回 access 和 refresh
    // commit('SET_TOKEN', token); // 你可能需要分别存储 access 和 refresh token
    // 假设后端 simplejwt 返回 { "access": "...", "refresh": "..." }
    if (response.data.access) {
        commit('SET_TOKEN', response.data.access); // 假设 SET_TOKEN 存储 access token
        // 你可能还需要一个 SET_REFRESH_TOKEN mutation 来存储 refresh token
        localStorage.setItem('user_refresh_token', response.data.refresh);
    } else if (response.data.token) { // 兼容只返回一个 token 的情况
        commit('SET_TOKEN', response.data.token);
    } else {
        throw new Error('Token not found in login response');
    }

    await dispatch('fetchCurrentUser');
    return response.data;
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.response?.data || 'Login failed';
    commit('SET_ERROR', errorMessage);
    throw new Error(errorMessage);
  }
},
  async fetchCurrentUser({ commit, state }) {
  if (!state.token) return; // 如果没有 token，则不获取
  commit('CLEAR_ERROR');
  try {
    // 原来的请求:
    // const response = await axios.get('/users/me/');
    // 修改后的请求 (匹配后端 accounts/urls.py 中的配置):
    const response = await axios.get('/accounts/me/'); // 使用新的正确路径
    commit('SET_CURRENT_USER', response.data);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch current user:', error);
    // Token 可能已过期或无效
    commit('LOGOUT'); // 清除无效 token 和用户信息
    const errorMessage = error.response?.data?.detail || 'Failed to fetch user data';
    commit('SET_ERROR', errorMessage);
    // throw new Error(errorMessage); // 可以选择性抛出
  }
},
  logoutUser({ commit }) {
    commit('LOGOUT');
    // await axios.post('/auth/logout/'); // 可选
  },

  // --- Admin User Management Actions ---
async fetchAllUsers({ commit }) {
  commit('SET_USER_LIST_LOADING', true);
  commit('CLEAR_ERROR');
  try {
    // const response = await axios.get('/users/'); // 原路径
    const response = await axios.get('/accounts/users/'); // 修改后的路径
    commit('SET_USERS', response.data.results || response.data);
    return response.data;
  } catch (error) {
    // ...
  } finally {
    commit('SET_USER_LIST_LOADING', false);
  }
},
async updateUserAdmin({ commit, dispatch }, { userId, data }) {
  commit('CLEAR_ERROR');
  try {
    // const response = await axios.put(`/users/${userId}/`, data); // 原路径
    const response = await axios.put(`/accounts/users/${userId}/`, data); // 修改后的路径
    dispatch('fetchAllUsers');
    console.log('User updated by admin', response.data);
    return response.data;
  } catch (error) {
    // ...
  }
},
async deleteUserAdmin({ commit, dispatch }, userId) {
  commit('CLEAR_ERROR');
  try {
    // await axios.delete(`/users/${userId}/`); // 原路径
    await axios.delete(`/accounts/users/${userId}/`); // 修改后的路径
    dispatch('fetchAllUsers');
    console.log(`User ${userId} deleted by admin`);
  }catch (error) {
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