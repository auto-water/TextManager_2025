from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label='确认密码')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "两次输入的密码不匹配。"})
        # 可以在这里添加其他邮箱或用户名的唯一性验证，但模型层面已经有了
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
            # 如果有 is_frozen 等字段，可以在这里设置或通过其他方式
        )
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    """用于显示用户详情和管理员操作"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_staff', 'is_active', 'is_frozen', 'date_joined')
        read_only_fields = ('date_joined', 'id') # 管理员可以修改 is_staff, is_active, is_frozen

class UserSimpleSerializer(serializers.ModelSerializer):
    """用于文章或评论中显示作者信息"""
    class Meta:
        model = User
        fields = ('id', 'username') # 'avatar' 如果有头像字段