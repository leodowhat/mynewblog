from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)
    content = models.TextField()
    abstract = models.CharField(max_length=300, blank=True)
    created_time = models.DateTimeField()
    last_modified_time = models.DateTimeField()

    category = models.ForeignKey(Category)
    # 假设一篇文章只有一个分类，但一个分类下可有多篇文章
    tags = models.ManyToManyField(Tag, blank=True)
    # 假设一篇文章可以有多个标签，一个标签下也有多篇文章
    author = models.ForeignKey(User)

    # 记录文章阅读量：
    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])
        # 只改变数据库中views字段的值
        
    # 自动截取文章以生成摘要：
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.abstract:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.abstract = strip_tags(md.convert(self.content))[:50]
            # 先将Markdown文本渲染成HTML文本，去掉HTML标签，摘取前50个字符赋给abstract，
        super(Post, self).save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

