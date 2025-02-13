from django import template
from django.shortcuts import get_object_or_404, render
from blog.models import Category ,Post, Comment, ReplyComment
from django.db.models import Count
from taggit.models import Tag

register = template.Library()

@register.inclusion_tag('blog/sidebar_post.html')
def popular_posts_tags(count=5, tag_slug=None):
    popular_posts = Post.published.annotate(total_comments=Count('comments')).order_by('?')[:count]
    category_list = Category.objects.annotate(total=Count('posts')).order_by('?')[:count]
    posts = Post.published.all()
    # Get common tags
    common_tags = Post.tags.most_common()[:10]
   
    context = {
        'popular_posts': popular_posts,
        'category_list': category_list,
        'posts': posts,
        'common_tags': common_tags
        
    }
    return context


@register.simple_tag
def count_comments(post):
    return Comment.objects.filter(post=post).count()

@register.simple_tag
def count_posts(category):
    return Post.objects.filter(category=category).count()
