from rest_framework import viewsets, permissions, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Article, Comment, Category
from .serializers import ArticleSerializer, CommentSerializer, CategorySerializer
from .permissions import IsAuthorOrReadOnly, IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated,  AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re
from zhipuai import ZhipuAI

class GenerateSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        content = request.data.get('content')
        if not content:
            return Response({'error': '文章内容不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        api_key = '5313f3660c534a2b97eb83ba02906a05.pyYdht4IRrzxQAaL'
        if not api_key:
            return Response({'error': 'API密钥未配置'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # 使用官方SDK调用
            client = ZhipuAI(api_key=api_key)
            response = client.chat.completions.create(
                model="glm-z1-flash",
                messages=[
                    {"role": "user", "content": f"生成这段内容的摘要，不要输出任何多余文字：{content}"}
                ],
                max_tokens=1000,
                temperature=0.2
            )
            
            if response.choices and response.choices[0].message.content:
                summary = response.choices[0].message.content

                # 使用正则表达式移除 <think> 标签及其内容
                summary = re.sub(r'<think>.*?</think>', '', summary, flags=re.DOTALL).strip()

                return Response({'summary': summary}, status=status.HTTP_200_OK)
            else:
                return Response({'error': '摘要生成失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            print(f'API调用异常: {str(e)}')
            return Response({'error': f'摘要生成失败: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related('author', 'category').all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # 从 filterset_fields 中移除 'category'，因为我们将自定义处理它
    filterset_fields = {
        'status': ['exact'],
        'author__username': ['exact', 'icontains'], # 示例：允许精确和包含查询
        # 'category': ['exact'], # 我们将手动处理 category
    }
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def _get_category_with_descendants(self, category_id):
        """
        辅助函数，获取给定分类ID及其所有子孙分类的ID列表。
        """
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return []

        descendant_ids = [category.id]
        
        # 简单递归获取子孙 (对于非常深的层级或大量数据，可能需要优化)
        # 或者使用 django-mptt 等库
        children = category.children.all()
        queue = list(children)
        
        while queue:
            child = queue.pop(0)
            descendant_ids.append(child.id)
            queue.extend(list(child.children.all()))
            
        return list(set(descendant_ids)) # 使用 set 去重（理论上不应该有重复）


    def get_queryset(self):
        queryset = super().get_queryset() # 获取基础 queryset
        user = self.request.user
        
        # 针对单篇文章的操作（详情、编辑、删除等）
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            article_id = self.kwargs.get('pk')
            if user.is_authenticated and article_id:
                # 允许用户访问：已发布的文章 或 自己的草稿
                from django.db.models import Q
                return Article.objects.filter(
                    Q(id=article_id) & (Q(status='published') | Q(status='draft', author=user))
                )
        
        # 处理列表请求
        status_filter = self.request.query_params.get('status')
        
        # 对草稿的处理：无论是否管理员，都只能看到自己的草稿
        if status_filter == 'draft':
            # 始终只显示自己的草稿，即使是管理员
            queryset = queryset.filter(author=user, status='draft')
        # 已发布文章的逻辑保持不变
        elif not user.is_staff:
            queryset = queryset.filter(status='published')
        
        # 处理作者筛选参数
        author_param = self.request.query_params.get('author')
        if author_param == 'me' and user.is_authenticated:
            # 使用当前登录用户的ID直接过滤
            queryset = queryset.filter(author_id=user.id)
            # 返回当前用户的文章
            return queryset
        
        # 其他筛选条件处理
        status_filter = self.request.query_params.get('status')
        
        if status_filter == 'draft':
            if not user.is_authenticated:
                return queryset.none()
            # 草稿只能看到自己的
            queryset = queryset.filter(author_id=user.id, status='draft')
        elif status_filter == 'published':
            queryset = queryset.filter(status='published')
        elif not user.is_staff:
            queryset = queryset.filter(status='published')

        # 自定义处理分类筛选
        category_id_param = self.request.query_params.get('category')
        if category_id_param:
            try:
                category_ids_to_filter = self._get_category_with_descendants(int(category_id_param))
                if category_ids_to_filter:
                    queryset = queryset.filter(category__id__in=category_ids_to_filter)
                else:
                    queryset = queryset.none()
            except ValueError:
                pass

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
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