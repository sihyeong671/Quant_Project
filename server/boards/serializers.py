from boards.models import Post
from rest_framework import serializers


from boards.models import Category


class CategorySerializer(serializers.ModelSerializer):
    favorite_count = serializers.SerializerMethodField(read_only=True)
    creator = serializers.CharField(source="creator.profile.nickname", read_only=True)
    
    class Meta:
        model = Category
        fields = (
            'id', 'title', 'created_date', 'top_fixed', 
            'favorite_count', 'creator',
        )
    
    def get_favorite_count(self, obj):
        return obj.favorite.all().count()


class PostSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField(read_only=True)
    creator = serializers.CharField(source="creator.profile.nickname", read_only=True)
    favorite_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        fields = (
            'id', 'title', 'content', 'thumbnail', 'hits',
            'created_date', 'modified_date', 'top_fixed',
            'creator', 'favorite_count',
        )
    
    def get_thumbnail(self, obj):
        try:
            return obj.thumbnail.url
        except:
            return ''
    
    def get_favorite_count(self, obj):
        return obj.favorite.all().count()


class PostDetailSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField(read_only=True)
    creator = serializers.SerializerMethodField(read_only=True)
    favorite_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        fields = (
            'id', 'thumbnail', 'title', 'content', 'hits', 'created_date', 
            'modified_date', 'creator', 'favorite_count',
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
        return obj.favorite.all().count()
    