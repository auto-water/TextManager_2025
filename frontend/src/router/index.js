// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

const RegisterPage = () => import('../views/RegisterPage.vue')
const LoginPage = () => import('../views/LoginPage.vue')

const HomePage = () => import('../views/HomePage.vue')
const ArticleEditor = () => import('../views/ArticleEditor.vue')
const DraftsPage = () => import('../views/DraftsPage.vue')
const ArticleDetail = () => import('../views/ArticleDetail.vue')
const MyArticlesPage = () => import('../views/MyArticlesPage.vue') // 新增导入
const CategoryManager = () => import('../views/CategoryManager.vue')
const AdminUserManager = () => import('../views/AdminUserManager.vue')
const ExplorePage = () => import('../views/ExplorePage.vue') // 新增导入
const NotFoundPage = () => import('../views/NotFoundPage.vue')


const routes = [
  { path: '/', redirect: '/home' },
  { path: '/register', name: 'Register', component: RegisterPage },
  { path: '/login', name: 'Login', component: LoginPage },
  {
    path: '/home',
    name: 'Home',
    component: HomePage,
    meta: { requiresAuth: false }
  },
  { // 新增路由
    path: '/explore',
    name: 'Explore',
    component: ExplorePage,
    meta: { requiresAuth: false } // 假设探索页无需登录
  },
  {
    path: '/editor/:id?',
    name: 'ArticleEditor',
    component: ArticleEditor,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/drafts',
    name: 'Drafts',
    component: DraftsPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/articles/:id',
    name: 'ArticleDetail',
    component: ArticleDetail,
    props: true,
    meta: { requiresAuth: false }
  },
  {
    path: '/my-articles',
    name: 'MyArticles',
    component: MyArticlesPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/categories',
    name: 'CategoryManager',
    component: CategoryManager,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'AdminUserManager',
    component: AdminUserManager,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundPage }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // 使用 Vite 的环境变量
  routes
})

// 全局前置守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters['user/isAuthenticated'];
  const currentUser = store.getters['user/currentUser']; // 获取当前用户信息

  if (to.meta.requiresAuth && !isAuthenticated) {
    // 如果需要认证但用户未登录
    next({ name: 'Login', query: { redirect: to.fullPath } }); // 跳转到登录页，并带上重定向参数
  } else if (to.meta.requiresAdmin && (!currentUser || !currentUser.is_staff)) {
    // 如果需要管理员权限但用户不是管理员
    // 可以跳转到首页或一个 "无权限" 页面
    console.warn('Access denied: Admin required.');
    next({ name: 'Home' }); // 或者 next(false) 阻止导航
  }
  else {
    next(); // 正常导航
  }
});

export default router