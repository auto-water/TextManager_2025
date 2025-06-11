# backend_project/urls.py (修改后)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework_simplejwt.views import TokenObtainPairView # 不再直接从这里导入用于登录
from accounts.views import CustomTokenObtainPairView # <<<--- 导入你的自定义视图
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('articles.urls')),

    # JWT 认证路由 - 使用自定义的视图
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # <<<--- 使用自定义视图
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)