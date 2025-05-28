from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    自定义权限，仅允许对象的所有者编辑它。
    读取权限对任何人开放（GET, HEAD, OPTIONS请求）。
    """
    def has_object_permission(self, request, view, obj):
        # 读取权限总是允许的
        if request.method in permissions.SAFE_METHODS:
            return True

        # 写入权限仅授予对象的所有者
        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    自定义权限，允许管理员进行写操作，其他人只读。
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff