import axios from 'axios'; // This will use the configured instance from main.js

// You can re-export the configured axios instance if needed elsewhere,
// or create specific functions for each endpoint.

// Example: User API
export const login = (credentials) => axios.post('/auth/token/', credentials);
export const register = (userData) => axios.post('/users/', userData); // or your dedicated /register/
export const fetchCurrentUser = () => axios.get('/users/me/'); // Assuming /me/ endpoint
// ... other user-related API calls

// Example: Article API
export const fetchArticles = (params) => axios.get('/articles/', { params });
export const fetchArticle = (id) => axios.get(`/articles/${id}/`);
export const createArticle = (data) => axios.post('/articles/', data);
export const updateArticle = (id, data) => axios.put(`/articles/${id}/`, data);
export const deleteArticle = (id) => axios.delete(`/articles/${id}/`);

// Example: Category API
export const fetchCategories = (params) => axios.get('/categories/', { params });
export const createCategory = (data) => axios.post('/categories/', data);
// ... etc.

// 添加响应拦截器
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
        console.error('未授权访问，可能是未登录或 Token 无效');
        // 跳转到登录页面或显示未登录提示
        window.location.href = '/login'; // 或者显示提示信息
        }
        return Promise.reject(error);
    }
);

export default apiClient;

// Then in your Vuex actions, you would import and use these:
// import * as api from '@/api';
// async loginUser({ commit }, credentials) {
//   const response = await api.login(credentials);
//   // ...
// }