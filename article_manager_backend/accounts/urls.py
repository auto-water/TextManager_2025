# accounts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationAPIView, CurrentUserAPIView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user-admin') # 管理员管理用户

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'), # 用户自注册
    path('me/', CurrentUserAPIView.as_view(), name='current-user'),
    path('', include(router.urls)), # 将 UserViewSet 相关的 URL 包含进来
]