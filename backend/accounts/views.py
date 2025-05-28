from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserRegistrationSerializer, UserDetailSerializer

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny] # 任何人都可以注册

# 如果需要自定义登录视图，可以继承 TokenObtainPairView
# class CustomTokenObtainPairView(TokenObtainPairView):
#     # serializer_class = CustomTokenObtainPairSerializer # 如果需要自定义序列化器

class CurrentUserAPIView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserViewSet(viewsets.ModelViewSet):
    """
    管理员用于管理用户。
    - 列出所有用户
    - 获取特定用户详情
    - 更新用户信息 (如 is_frozen, is_staff)
    - 删除用户
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAdminUser] # 仅管理员可访问

    # 注意：ModelViewSet 默认的 create 方法不适合于用户注册（密码处理等）
    # 用户注册使用 UserRegistrationAPIView。
    # 如果要通过此 ViewSet 创建用户（管理员创建），需要自定义 create 方法或确保序列化器正确处理密码。
    # 通常管理员创建用户时，密码会随机生成或通过其他方式设置，而不是直接输入。
    # 此处的 create 方法会被 `POST /api/users/` (来自 router.register) 调用，而文档中此接口用于用户自注册
    # 因此，UserViewSet 的 create 应该被禁用或有特殊处理，或者用户自注册走单独的 /register/ 路径

    # 禁用 UserViewSet 的 create, partial_update (用 update 即可)
    # http_method_names = ['get', 'put', 'delete', 'head', 'options'] # 移除 post, patch

    # 或者在UserDetailSerializer中对password字段进行特殊处理，使其在管理员编辑时不必须，创建时哈希