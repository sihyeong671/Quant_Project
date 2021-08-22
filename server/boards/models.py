from django.db import models

from users.models import User


class Category(models.Model):
    title = models.CharField(max_length=128, null=True, blank=False)
    is_anonymous = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    top_fixed = models.BooleanField(default=False)
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="category")
    favorite = models.ManyToManyField(User, blank=True, related_name='favorite_category')
    
    class Meta:
        verbose_name = '게시판 종류'
        verbose_name_plural = '게시판 종류 모음'
        ordering = ['-title', ]
        
    def __str__(self):
        return self.title
    

class Board(models.Model):
    title = models.CharField(max_length=128, null=True, blank=False)
    content = models.TextField(null=True, blank=False)
    thumbnail = models.ImageField(upload_to='board_thumbnail/', null=True, blank=True)
    hits = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    top_fixed = models.BooleanField(default=False)
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="board")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="board")
    favorite = models.ManyToManyField(User, blank=True, related_name='favorite_board')
    
    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '게시글 모음'
        ordering = ['-category__title', ]
        
    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField(null=True, blank=False)
    
    creator = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="comment")
    

class Reply(models.Model):
    content = models.TextField(null=True, blank=False)
    
    creator = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reply")
    