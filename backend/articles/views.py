from rest_framework import viewsets, permissions, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Comment, Category
from .serializers import ArticleSerializer, CommentSerializer, CategorySerializer
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author', 'category').all() # 优化查询
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'author__username'] # 按分类、状态、作者用户名过滤
    search_fields = ['title', 'content', 'excerpt'] # 按标题、内容、摘要搜索
    ordering_fields = ['created_at', 'updated_at', 'title'] # 可排序字段

    def get_queryset(self):
        queryset = super().get_queryset()
        # 普通用户只能看到已发布的文章，或者自己的草稿
        if not self.request.user.is_staff: # 如果不是管理员
            if self.action == 'list': # 列表视图
                # 如果是草稿箱请求，则只返回当前用户的草稿
                status_filter = self.request.query_params.get('status')
                if status_filter == 'draft':
                    return queryset.filter(author=self.request.user, status='draft')
                # 否则只返回已发布的
                return queryset.filter(status='published')
            # 对于详情视图，如果是草稿，只有作者能看
            # 这个逻辑最好放在 has_object_permission 中，但这里也可以简单处理
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        # 确保只有作者或管理员可以更新
        # IsAuthorOrReadOnly 权限类已经处理了这个
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'article').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['article'] # 按文章ID过滤评论

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # 管理员可增删改查，普通用户只读
    permission_classes = [IsAdminOrReadOnly]

    # 如果需要支持三级分类的创建，例如前端传递 parent_id
    # CategorySerializer 已经配置了 parent_id 为 write_only