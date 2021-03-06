from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from boards.models import Category, Post, Comment, Reply


class CategorySerializer(serializers.ModelSerializer):
    # favorite_count = serializers.SerializerMethodField(read_only=True)
    creator = serializers.CharField(source="creator.profile.nickname", read_only=True)
    
    class Meta:
        model = Category
        fields = (
            'id', 'title', 'created_date', 'top_fixed', 
             'creator',
        )
    
    # def get_favorite_count(self, obj):
    #     return obj.favorite.all().count()


class PostListSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField(read_only=True)
    creator = serializers.SerializerMethodField(read_only=True)
    favorite_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        fields = (
            'id', 'category', 'title', 'content', 'thumbnail', 
            'hits', 'created_date', 'modified_date', 'top_fixed',
            'creator', 'favorite_count',
        )
    
    def get_creator(self, obj):
        try:
            category = obj.category
            creator = obj.creator
            is_anonymous = category.is_anonymous
            if is_anonymous:
                return "익명"
            else:
                return creator.profile.nickname
        except:
            return ''
    
    def get_thumbnail(self, obj):
        try:
            return obj.thumbnail.url
        except:
            return ''
    
    def get_favorite_count(self, obj):
        try:
            favorites = obj.favorite.all()
            return favorites.count()
        except:
            return 0


class ReplySerializer(serializers.ModelSerializer):
    creator = serializers.SerializerMethodField(read_only=True)
    favorite_count = SerializerMethodField(read_only=True)
    
    class Meta:
        model = Reply
        fields = (
            'id', 'content', 'creator', 'favorite_count',
        )
        
    def get_creator(self, obj):
        is_anonymous = obj.comment.post.category.is_anonymous
        if is_anonymous:
            return "익명"
        else:
            return obj.creator.profile.nickname
    
    def get_favorite_count(self, obj):
        try:
            return obj.favorite.all().count()
        except:
            return 0


class CommentSerializer(serializers.ModelSerializer):
    reply = ReplySerializer(many=True, read_only=True)
    creator = SerializerMethodField(read_only=True)
    favorite_count = SerializerMethodField(read_only=True)
    
    class Meta:
        model = Comment
        fields = (
            'id', 'content', 'creator', 'favorite_count', 'reply', 
        )
        
    def get_creator(self, obj):
        is_anonymous = obj.post.category.is_anonymous
        # is_anonymous = True
        if is_anonymous:
            return "익명"
        else:
            return obj.creator.profile.nickname
    
    def get_favorite_count(self, obj):
        try:
            return obj.favorite.all().count()
        except:
            return 0


class PostDetailSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(many=True, read_only=True)
    thumbnail = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()
    favorite_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        fields = (
            'id', 'thumbnail', 'title', 'content', 'hits', 'created_date', 
            'modified_date', 'creator', 'favorite_count', 'comment',
        )
    
    def get_creator(self, obj):
        is_anonymous = obj.category.is_anonymous
        if is_anonymous:
            return "익명"
        else:
            return obj.creator.profile.nickname
    
    def get_thumbnail(self, obj):
        try:
            return obj.thumbnail.url
        except:
            return ''
    
    def get_favorite_count(self, obj):
        try:
            return obj.favorite.all().count()
        except:
            return 0
    