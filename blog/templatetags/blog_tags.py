from django import template
from ..models import Post, Tag, Category

from django.db.models.aggregates import Count

register = template.Library()
# 必须用register这个单词实例化


# 最新文章模板标签
@register.simple_tag()
# 将get_recent_posts函数装饰为rigister.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-created_time')[:num]


# 归档模板标签
@register.simple_tag
def archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


# 分类模板标签
@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


# 标签云
@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
