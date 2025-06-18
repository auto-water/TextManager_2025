# 文章管理系统

这个系统是一个功能完整的文章管理平台，包含前端Vue.js应用和后端Django REST API。

## 系统功能

- 用户管理（注册、登录、权限控制）
- 文章管理（创建、编辑、发布、删除）
- 分类管理（多级分类）
- 评论系统
- AI摘要生成

## 技术栈

### 前端
- Vue 3
- Vuex 4
- Vue Router
- Axios
- Vite

### 后端
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- ZhipuAI (智谱AI)

## 运行项目

### 1. 数据库配置

本项目使用PostgreSQL数据库，请确保已安装PostgreSQL。

```bash
# 安装PostgreSQL (Ubuntu示例)
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Windows用户可以从官网下载安装包：
# https://www.postgresql.org/download/windows/

# 创建数据库和用户
sudo -u postgres psql

postgres=# CREATE USER dbuser WITH PASSWORD '123456';
postgres=# CREATE DATABASE article_manager_db OWNER dbuser;
postgres=# ALTER USER dbuser CREATEDB;
postgres=# \q
```

### 2. 后端配置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖包
pip install -r requirements.txt

# 应用数据库迁移
python manage.py migrate

# 运行开发服务器
python manage.py runserver
```

如需修改数据库配置，编辑 settings.py 文件：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'article_manager_db',  # 数据库名称
        'USER': 'dbuser',              # 数据库用户名
        'PASSWORD': '123456',          # 数据库密码
        'HOST': 'localhost',           # 数据库主机地址
        'PORT': '5432',                # PostgreSQL 默认端口
    }
}
```

### 3. 前端配置

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 运行开发服务器
npm run dev
```

## 访问系统

- 前端: http://localhost:5173/
- 后端API: http://localhost:8000/api/
- 管理后台: http://localhost:8000/admin/

## API端点

### 认证
- POST /api/accounts/register/: 用户注册
- POST /api/token/: 获取JWT令牌
- POST /api/token/refresh/: 刷新JWT令牌

### 文章
- GET /api/articles/: 获取文章列表
- POST /api/articles/: 创建文章
- GET /api/articles/{id}/: 获取文章详情
- PUT/PATCH /api/articles/{id}/: 更新文章
- DELETE /api/articles/{id}/: 删除文章

### 分类
- GET /api/categories/: 获取分类列表
- POST /api/categories/: 创建分类
- GET /api/categories/{id}/: 获取分类详情
- PUT/PATCH /api/categories/{id}/: 更新分类
- DELETE /api/categories/{id}/: 删除分类

### 评论
- GET /api/comments/: 获取评论列表
- POST /api/comments/: 创建评论
- DELETE /api/comments/{id}/: 删除评论

### 用户管理
- GET /api/accounts/me/: 获取当前用户信息
- GET /api/accounts/users/: 获取用户列表(管理员)
- PATCH /api/accounts/users/{id}/: 更新用户(管理员)
- DELETE /api/accounts/users/{id}/: 删除用户(管理员)

### AI功能
- POST /api/generate-summary/: 生成文章摘要

## 注意事项

1. 确保在生产环境中更改Django的SECRET_KEY
2. 更新CORS设置以匹配您的生产域名
3. 为智谱AI API设置有效的密钥