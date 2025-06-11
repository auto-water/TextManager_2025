# accounts/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer # 导入
from django.utils.translation import gettext_lazy as _ # 用于错误信息国际化 (可选)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label='确认密码')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "两次输入的密码不匹配。"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    """用于显示用户详情和管理员操作"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_active', 'is_frozen', 'date_joined')
        read_only_fields = ('date_joined', 'id')

class UserSimpleSerializer(serializers.ModelSerializer):
    """用于文章或评论中显示作者信息"""
    class Meta:
        model = User
        fields = ('id', 'username')


# --- 新增/修改部分 开始 ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # 你可以在这里向 token payload 添加自定义声明 (如果需要)
        # 例如: token['username'] = user.username
        return token

    def validate(self, attrs):
        # 调用父类的 validate 方法，它会检查 is_active 和密码
        data = super().validate(attrs)

        # 父类验证成功后，self.user 就是被认证的用户对象
        if self.user and self.user.is_frozen:
            # 如果用户被冻结，则引发验证错误，阻止登录
            raise serializers.ValidationError(
                # 使用 _() 进行翻译，如果你的项目配置了国际化
                # "此账户已被冻结，无法登录。"
                {"detail": _("此账户已被冻结，无法登录。")}, # 返回更标准的错误格式
                code='account_frozen',
            )
        # 如果用户未被冻结，则正常返回父类验证后的数据 (包含 token)
        return data
# --- 新增/修改部分 结束 ---