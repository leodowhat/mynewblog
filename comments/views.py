# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm


def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # commit=False的作用是仅仅利用表单的数据生成Comment模型类的实例，而不保存评论数据到数据库
            comment.post = post
            # 上述语句：将评论与对应文章关联起来
            comment.save()
            return redirect(post)
        else:
            comment_list = post.comment_set.all()
            # 获取该post对应的全部评论
            context = {
                'post': post,
                'form': form,
                'comment_list': comment_list
            }
            return render(request, 'blog/detail.html', context=context)
    return redirect(post)
    # 不是POST请求时，说明用户没有提交数据，则重定向到文章详情页


