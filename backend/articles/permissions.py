from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    自定义权限，允许对象的所有者或管理员编辑/删除它。
    读取权限对任何人开放（GET, HEAD, OPTIONS请求）。
    """
    def has_object_permission(self, request, view, obj):
        # 读取权限总是允许的
        if request.method in permissions.SAFE_METHODS:
            return True

        # 写入权限授予对象的所有者或管理员用户
        # obj.author 是文章的作者
        # request.user 是当前发出请求的用户
        return obj.author == request.user or request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    自定义权限，允许管理员进行写操作，其他人只读。
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff