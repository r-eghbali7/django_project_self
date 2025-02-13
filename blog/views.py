from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from .models import Post, Category, Comment, ReplyComment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag
from .forms import CommentForm, ReplyCommentForm
from django.contrib.auth.decorators import login_required

@login_required
def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    post_list = Post.published.all()
    posts = Post.objects.filter(category=category)
    
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get('page', 1)
    category_posts = paginator.page(page_number)
    return render(request, 'blog/category_list.html', {'category': category, 'category_posts': category_posts, 'posts':posts})


def post_list(request, tag_slug=None):
    # ابتدا فیلتر بر اساس تگ (اگر تگ وجود داشته باشد)
    post_list = Post.published.all()
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    
    # صفحه‌بندی با 1 پست در هر صفحه
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
        
    # بازگشت به قالب
    return render(request, 'blog/post_list.html', {
        'posts': posts,  # ارسال پست‌های صفحه‌بندی‌شده  # شماره صفحه
        'tag_slug': tag_slug , # ارسال پارامتر تگ در صورت فیلتر
    })



def post_detail(request,slug, year, month, day):
    post = get_object_or_404(Post,status=Post.STATUS.PUBLISHED, slug=slug, created_date__year=year, created_date__month=month, created_date__day=day)
    comments = Comment.objects.filter(post=post)
    reply_comments = ReplyComment.objects.filter(comment__post=post)
    next_post = Post.objects.filter(created_date__gt=post.created_date).order_by('created_date').first()
    prev_post = Post.objects.filter(created_date__lt=post.created_date).order_by('-created_date').first()
    
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            body = form.cleaned_data['body']
            comment = Comment(name=name, email=email, body=body, post=post)
            comment.save()
            return HttpResponse('نظر شما با موفقیت ثبت شد')
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'reply_comments': reply_comments,
        'next_post': next_post,
        'prev_post': prev_post,
        'form': form,
    }
    return render(request, 'blog/post_detail.html', context)
    

def post_new(request):
    return render(request, 'blog/post_new.html', {})


def post_edit(request):
    return render(request, 'blog/post_edit.html', {})


def comment_form(request, post_id):
    post_item = get_object_or_404(Post, id=post_id)
