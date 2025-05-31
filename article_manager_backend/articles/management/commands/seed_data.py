# articles/management/commands/seed_data.py
import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from articles.models import Category, Article, Comment
from faker import Faker # 用于生成伪数据，需要安装: pip install Faker

User = get_user_model()
fake = Faker('zh_CN') # 使用中文伪数据

class Command(BaseCommand):
    help = 'Seeds the database with sample data for articles, categories, and comments.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to seed data...'))

        # 清理旧数据 (可选，但方便重复执行脚本)
        self.stdout.write('Clearing old data...')
        Comment.objects.all().delete()
        Article.objects.all().delete()
        Category.objects.all().delete()
        # User.objects.filter(is_superuser=False).delete() # 清除非超级用户，谨慎操作

        # --- 创建用户 ---
        self.stdout.write('Creating users...')
        users = []
        # 创建一个管理员用户 (如果还没有)
        admin_user, created = User.objects.get_or_create(
            username='admin_seed',
            defaults={
                'email': 'admin_seed@example.com',
                'is_staff': True,
                'is_superuser': False, # 不是超级用户，只是普通管理员
                'is_frozen': False,
            }
        )
        if created:
            admin_user.set_password('adminpassword')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin_user.username}'))
        users.append(admin_user)


        for i in range(5): # 创建 5 个普通用户
            username = fake.user_name()
            while User.objects.filter(username=username).exists(): # 确保用户名唯一
                username = fake.user_name() + str(random.randint(1,100))

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': fake.email(),
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'is_frozen': random.choice([True, False, False]), # 随机冻结一些
                }
            )
            if created:
                user.set_password('testpassword123')
                user.save()
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users.'))


        # --- 创建分类 (三级结构) ---
        self.stdout.write('Creating categories...')
        categories_data = [
            {'name': '技术', 'children': [
                {'name': '编程语言', 'children': [
                    {'name': 'Python'}, {'name': 'JavaScript'}, {'name': 'Java'}
                ]},
                {'name': '数据库', 'children': [
                    {'name': 'PostgreSQL'}, {'name': 'MySQL'}, {'name': 'MongoDB'}
                ]},
                {'name': 'Web开发'}
            ]},
            {'name': '生活', 'children': [
                {'name': '美食', 'children': [
                    {'name': '中餐'}, {'name': '西餐'}
                ]},
                {'name': '旅行'}
            ]},
            {'name': '哲学'}
        ]

        created_categories = {} # 用于存储创建的分类对象，方便后续查找

        def create_categories_recursive(data_list, parent=None):
            for cat_data in data_list:
                category, created = Category.objects.get_or_create(
                    name=cat_data['name'],
                    defaults={'parent': parent}
                )
                created_categories[cat_data['name']] = category # 存储对象
                if 'children' in cat_data:
                    create_categories_recursive(cat_data['children'], parent=category)

        create_categories_recursive(categories_data)
        all_categories = list(Category.objects.all()) # 获取所有创建的分类
        self.stdout.write(self.style.SUCCESS(f'Created {Category.objects.count()} categories.'))

        if not all_categories:
            self.stdout.write(self.style.WARNING('No categories created, articles might not have categories.'))
            # 可以创建一个默认分类
            default_cat, _ = Category.objects.get_or_create(name='未分类')
            all_categories.append(default_cat)


        # --- 创建文章 ---
        self.stdout.write('Creating articles...')
        num_articles = 25
        for i in range(num_articles):
            author = random.choice(users)
            category = random.choice(all_categories) if all_categories else None
            status = random.choice([Article.STATUS_CHOICES[0][0], Article.STATUS_CHOICES[1][0], Article.STATUS_CHOICES[1][0]]) # 更多已发布

            title = fake.sentence(nb_words=random.randint(4, 10)).rstrip('.')
            # 确保标题唯一性 (简单处理，对于大量数据可能需要更健壮的方法)
            original_title = title
            count = 0
            while Article.objects.filter(title=title).exists():
                count += 1
                title = f"{original_title} ({count})"


            article_content_paragraphs = [fake.paragraph(nb_sentences=random.randint(5,15)) for _ in range(random.randint(3,7))]
            article_content = "\n\n".join(article_content_paragraphs)

            excerpt_sentences = random.sample(article_content_paragraphs[0].split('. '), k=min(2, len(article_content_paragraphs[0].split('. '))))
            excerpt = ". ".join(excerpt_sentences) + "." if excerpt_sentences else ""


            Article.objects.create(
                title=title,
                content=article_content,
                excerpt=excerpt,
                author=author,
                category=category,
                status=status,
                # cover_image 稍后可以考虑添加
            )
        self.stdout.write(self.style.SUCCESS(f'Created {num_articles} articles.'))


        # --- 创建评论 ---
        self.stdout.write('Creating comments...')
        all_articles = list(Article.objects.filter(status='published')) # 只对已发布的文章评论
        num_comments_total = 50
        if all_articles:
            for _ in range(num_comments_total):
                article = random.choice(all_articles)
                author = random.choice(users)
                Comment.objects.create(
                    article=article,
                    author=author,
                    content=fake.sentence(nb_words=random.randint(5, 25))
                )
            self.stdout.write(self.style.SUCCESS(f'Created {num_comments_total} comments.'))
        else:
            self.stdout.write(self.style.WARNING('No published articles to comment on.'))


        self.stdout.write(self.style.SUCCESS('Successfully seeded data!'))