from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from .models import Post


def post_list(request):
    try:
        posts = Post.published.all()
    except:
        return HttpResponse("DONT HAVE POSTS")
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request,slug, year, month, day):
    post = get_object_or_404(Post,status=Post.STATUS.PUBLISHED, slug=slug, created_date__year=year, created_date__month=month, created_date__day=day)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    return render(request, 'blog/post_new.html', {})


def post_edit(request):
    return render(request, 'blog/post_edit.html', {})


