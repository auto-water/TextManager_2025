from django.db import models
from django.conf import settings # 用于关联 User 模型

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称')
    # 自关联，用于实现多级分类
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL, # 父分类删除时，子分类的 parent 设为 NULL
        related_name='children',
        verbose_name='父级分类'
    )

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        # 显示层级关系
        path = [self.name]
        p = self.parent
        while p is not None:
            path.append(p.name)
            p = p.parent
        return ' -> '.join(reversed(path))


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]

    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    excerpt = models.TextField(blank=True, verbose_name='摘要') # 可选摘要
    cover_image = models.ImageField(upload_to='article_covers/', null=True, blank=True, verbose_name='封面图片') # 可选封面

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # 作者删除时，其文章也删除
        related_name='articles',
        verbose_name='作者'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL, # 分类删除时，文章的分类设为 NULL
        related_name='articles',
        verbose_name='分类'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_at'] # 默认按创建时间降序

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments', # 方便从文章反向查询评论
        verbose_name='所属文章'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # 评论者删除时，其评论也删除
        related_name='comments',
        verbose_name='评论者'
    )
    content = models.TextField(verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    # 可以添加父评论，实现评论回复功能
    # parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['created_at'] # 默认按评论时间升序

    def __str__(self):
        return f'Comment by {self.author.username} on {self.article.title}'