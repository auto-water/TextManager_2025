from rest_framework import serializers
from .models import Article, Comment, Category
from accounts.serializers import UserSimpleSerializer # 引入简化的用户序列化器

class RecursiveCategorySerializer(serializers.Serializer):
    """用于递归显示子分类 (辅助，实际可能不用这么复杂)"""
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CategorySerializer(serializers.ModelSerializer):
    # 用于接收前端传来的 parent_id (创建/更新时)
    # source='parent' 意味着它会作用于模型的 'parent' 字段
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        allow_null=True, # 顶级分类的 parent 是 null
        required=False   # 创建顶级分类时不需要提供 parent
    )
    # parent_details 仍然可以保留，用于前端可能需要显示父分类名称等详细信息
    parent_details = serializers.SerializerMethodField(read_only=True)
    children_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'parent',         # <--- 核心改动：直接输出 parent 字段 (其值为父ID或null)
            'parent_details',
            'children_count'
        ]

    def get_parent_details(self, obj):
        if obj.parent:
            return {'id': obj.parent.id, 'name': obj.parent.name}
        return None

    def get_children_count(self, obj):
        return obj.children.count()


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)
    # category = CategorySerializer(read_only=True) # 读取时显示分类详情
    # category_id = serializers.PrimaryKeyRelatedField(
    #     queryset=Category.objects.all(), source='category', write_only=True, allow_null=True, required=False
    # )
    category_details = CategorySerializer(source='category', read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True, allow_null=True, required=False
    )


    class Meta:
        model = Article
        fields = [
            'id', 'title', 'content', 'excerpt', 'cover_image',
            'author', 'category', 'category_details', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('author', 'created_at', 'updated_at', 'category_details')

    # 如果需要自定义创建或更新逻辑，可以重写 create/update 方法
    # 例如，在前端没有传 excerpt 时自动生成
    # def create(self, validated_data):
    #     if not validated_data.get('excerpt') and validated_data.get('content'):
    #         validated_data['excerpt'] = validated_data['content'][:150] + "..." # 简单摘要
    #     return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)
    article = serializers.PrimaryKeyRelatedField(queryset=Article.objects.all()) # 写入时关联文章ID

    class Meta:
        model = Comment
        fields = ['id', 'article', 'author', 'content', 'created_at']
        read_only_fields = ('author', 'created_at')