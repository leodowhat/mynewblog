# -*- coding: utf-8 -*-

from django.contrib.syndication.views import Feed

from .models import Post



class AllPostRssFeed(Feed):
    title = "Django 博客教程演示项目"

    link = "/"
    # 通过聚合阅读器跳转的网址

    description = "Django博客测试文章"

    # 需要演示的内容条目
    def items(self):
        return Post.objects.all()

    # 聚合器中显示的内容条目的标题
    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    # 聚合器中显示的内容条目的概述
    def item_description(self, item):
        return item.content
