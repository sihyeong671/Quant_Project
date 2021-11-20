from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL
# User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=128, unique=True, null=True, blank=False)
    is_anonymous = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    top_fixed = models.BooleanField(default=False)
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="category")
    
    class Meta:
        verbose_name = '게시판 종류'
        verbose_name_plural = '게시판 종류 모음'
        ordering = ['-created_date', ]
        
    def __str__(self):
        return self.title
    

class Post(models.Model):
    title = models.CharField(max_length=128, null=True, blank=False)
    content = models.TextField(default='', null=True, blank=False)
    thumbnail = models.ImageField(upload_to='post_thumbnail/', null=True, blank=True)
    hits = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    top_fixed = models.BooleanField(default=False)
    
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name="post")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    
    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '게시글 모음'
        ordering = ['-category__title', ]
        
    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(null=True, blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")
    
    class Meta:
        verbose_name_plural = '댓글'
    
    def __str__(self):
        return self.content
    

class Reply(models.Model):
    content = models.TextField(null=True, blank=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reply")
    comment = models.ForeignKey(Comment, null=True, on_delete=models.DO_NOTHING, related_name="reply")
    
    class Meta:
        verbose_name_plural = '대댓글'
    
    def __str__(self):
        return self.content