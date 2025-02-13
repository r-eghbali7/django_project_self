from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinLengthValidator, EmailValidator, RegexValidator
from taggit.managers import TaggableManager

class ManagerPost(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.STATUS.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        indexes = [
            models.Index(fields=['name']),
        ]

    def get_absolute_url(self):
        return reverse("blog:category_list", args=[self.slug])


class Post(models.Model):
    class STATUS(models.TextChoices):
        DRAFT = 'draft',
        PUBLISHED = 'published'
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts', verbose_name='دسته بندی')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True, db_index=True, verbose_name='عنوان')
    text = models.TextField(verbose_name='متن')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='تاریخ ایجاد')
    update_date = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name='تاریخ بروزرسانی')
    status = models.CharField(max_length=10, choices=STATUS.choices, default=STATUS.DRAFT, verbose_name='وضعیت انتشار')
    slug = models.SlugField(max_length=250, unique_for_date='created_date', verbose_name='آدرس')
    
    tags = TaggableManager()
    objects = models.Manager()
    published = ManagerPost()

    def __str__(self):
        return f'{self.title} - {self.author}'
    
    class Meta:
        ordering = ['-created_date']
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'
        indexes = [
            models.Index(fields=['-created_date']),
        ]
        
    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.created_date.year,self.created_date.month,self.created_date.day,self.slug])



class BaseCommentFields(models.Model):
    NAME_VALIDATORS = [
        MinLengthValidator(2, 'Name must be at least 2 characters long'),
        RegexValidator(
            regex=r'^[a-zA-Z\s\u0600-\u06FF]+$',
            message='Name can only contain letters and spaces'
        )
    ]
    
    EMAIL_VALIDATORS = [
        RegexValidator(
            regex=r'^[a-zA-Z0-9._%+-]+@gmail\.com$',
            message='Email must be a valid Gmail address'
        )
    ]
    
    BODY_VALIDATORS = [
        MinLengthValidator(5, 'Comment must be at least 5 characters long'),
        RegexValidator(
            regex=r'^[a-zA-Z0-9\s\u0600-\u06FF.,!?()-]+$',
            message='Comment contains invalid characters'
        )
    ]

    name = models.CharField(max_length=80, validators=NAME_VALIDATORS)
    email = models.EmailField(validators=EMAIL_VALIDATORS)
    body = models.TextField(validators=BODY_VALIDATORS)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Comment(BaseCommentFields):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='پست')
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
        indexes = [models.Index(fields=['-created'])]

class ReplyComment(BaseCommentFields):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', verbose_name='کامنت')
    
    class Meta:
        ordering = ['-created']
        verbose_name = 'پاسخ کامنت'
        verbose_name_plural = 'پاسخ کامنت ها'
        indexes = [models.Index(fields=['-created'])]

