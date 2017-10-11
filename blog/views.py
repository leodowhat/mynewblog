# -*- coding: utf-8 -*-

import markdown
from django.views.generic import ListView

from django.shortcuts import render, get_object_or_404
from .models import Post, Tag, Category
from comments.forms import CommentForm


def index(request):
    article_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={
        'article_list': article_list
    })

#     使用类视图如下：


class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    paginate_by = 1
    # 开启分页功能，设置每个页面3篇文章


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.content = markdown.markdown(post.content,
                            extensions = {
                                'markdown.extensions.extra',
                                'markdown.extensions.codehilite',
                                'markdown.extensions.toc'
                            })
    # 每次调用视图中的detail函数,则阅读量加1：
    post.increase_views()

    # 评论表单部分：

    form = CommentForm()
    comment_list = post.comment_set.all()
    # 获取这边文章的全部评论
    context = {
        'post': post,
        'form': form,
        'comment_list': comment_list
    }

    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):
    article_list = Post.objects.filter(
        created_time__year=year,
        created_time__month=month,
        # 此处按照Python语法应该是created_time.year,但由于这里
        # 作为函数的参数列表，所以Django要求把点运算符替换成两个下划线
    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={
        'article_list': article_list
    })

#     使用类视图如下：


class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    article_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={
        'article_list': article_list
    })

#     使用类视图如下：


class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    # 直接继承文章列表的IndexView类视图
    def get_queryset(self):
        # 覆盖了父类的get_queryset
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        # 注意:URL捕获的参数，命名组保存在kwargs属性中（字典）；非命名组保存在args属性中（列表）
        return super(CategoryView, self).get_queryset().filter(category=cate)

class TagView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)
