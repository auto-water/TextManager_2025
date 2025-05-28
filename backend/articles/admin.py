from django.contrib import admin
from .models import Article, Comment, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'id')
    search_fields = ('name',)
    list_filter = ('parent',)
    # 可以使用 django-mptt 或类似库来更好地管理树形结构

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'category', 'author')
    search_fields = ('title', 'content', 'author__username')
    date_hierarchy = 'created_at'
    raw_id_fields = ('author', 'category') # 对于外键很多的情况，使用 ID 输入框

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_preview', 'author', 'article', 'created_at')
    list_filter = ('author', 'article')
    search_fields = ('content', 'author__username', 'article__title')
    date_hierarchy = 'created_at'
    raw_id_fields = ('author', 'article')

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = '评论内容预览'