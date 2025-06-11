from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='邮箱地址') # 确保邮箱唯一
    is_frozen = models.BooleanField(default=False, verbose_name='是否冻结')
    # 可以添加其他字段，如头像、简介等
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    # bio = models.TextField(max_length=500, blank=True)

    # 如果使用 email 作为登录字段，需要修改 USERNAME_FIELD 和 REQUIRED_FIELDS
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username'] # 如果 email 是 USERNAME_FIELD，username 可能是可选的

    def __str__(self):
        return self.username