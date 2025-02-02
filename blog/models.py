from django.db import models
from django.urls import reverse
from django.utils import timezone


class ManagerPost(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.STATUS.PUBLISHED)


class Post(models.Model):
    class STATUS(models.TextChoices):
        DRAFT = 'draft',
        PUBLISHED = 'published'
    
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS.choices, default=STATUS.DRAFT)
    slug = models.SlugField(max_length=250, unique_for_date='created_date')

    objects = models.Manager()
    published = ManagerPost()

    def __str__(self):
        return f'{self.title} - {self.author}'
    
    class Meta:
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['-created_date']),
        ]
        
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.created_date.year,self.created_date.month,self.created_date.day,self.slug])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    
    