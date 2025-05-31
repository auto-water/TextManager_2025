from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')), # 注意这里的前缀
    path('api/', include('articles.urls')), # 将文章、分类、评论 API 放在 /api/ 下

    # JWT 认证路由
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # 获取 token (登录)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # 刷新 token
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),    # 验证 token

    # DRF Token Auth (如果使用)
    # path('api/auth/', include('rest_framework.urls')), # DRF 登录/登出 (基于 Session)
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'), # DRF Token
]

# 开发环境下提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)