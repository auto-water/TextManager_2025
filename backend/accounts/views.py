# accounts/views.py
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView # 导入
from .models import User
# 从 .serializers 导入所有需要的序列化器，包括新增的
from .serializers import (
    UserRegistrationSerializer,
    UserDetailSerializer,
    CustomTokenObtainPairSerializer # 导入自定义序列化器
)

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

class CurrentUserAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser]


# --- 新增/修改部分 开始 ---
# 创建一个使用自定义序列化器的 TokenObtainPairView
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
# --- 新增/修改部分 结束 ---