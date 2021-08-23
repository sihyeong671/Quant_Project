from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from api.mixins import PublicApiMixin, ApiAuthMixin

from boards.serializers import CategorySerializer, PostSerializer,\
    PostDetailSerializer
from boards.models import Category, Post, Comment, Reply


class CategoryCreateReadApi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        category = Category(
            creator=request.user, 
            title=request.data.get('title', ''),
            is_anonymous=request.data.get('anonymous', False)
        )
        
        category.save()
        
        return Response({
            "message": "Category created success"
        }, status=status.HTTP_201_CREATED)


class CategoryDeleteAndPostListApi(ApiAuthMixin, APIView):
    def delete(self, request, *args, **kwargs):
        pk = kwargs['cate_id']
        category = get_object_or_404(Category, pk=pk)
        
        if request.user != category.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
        
        if category.post.all().count() > 0:
            return Response({
                "message": "Post exists"
            }, status=status.HTTP_403_FORBIDDEN)
        
        category.delete()
        
        return Response({
            "message": "Category delete success"
        }, status=status.HTTP_200_OK)
        
        
    def get(self, request, *args, **kwargs):
        pk = kwargs['cate_id']
        
        if not pk:
            return Response({
                "message": "Select a board type"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        category = Category.objects.get(pk=pk)
        postlist = Post.objects.filter(category=category)
        
        serializer = PostSerializer(postlist, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostCreateApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        cate_id = kwargs['cate_id']
        category = get_object_or_404(Category, pk=cate_id)
        
        title = request.data.get('title', '')
        content = request.data.get('content', '')
        
        if title == '' or content == '':
            return Response({
                "message": "title required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        post = Post(
            creator=request.user, 
            category=category,
            title=title,
            content=content,
            thumbnail=request.data.get('thumbnail', '')
        )
        
        post.save()
        
        return Response({
            "message": "Post created success"
        }, status=status.HTTP_201_CREATED)


class PostManageAPi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs['post_id']
        post = get_object_or_404(Post, pk=pk)
        serializer = PostDetailSerializer(post, many=False, allow_null=True)
        print(serializer)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        expire_time = 600
        cookie_value = request.COOKIES.get('hitboard', '_')

        if f'_{pk}_' not in cookie_value:
            cookie_value += f'{pk}_'
            response.set_cookie('hitboard', value=cookie_value, max_age=expire_time, httponly=True)

            post.hits += 1
            post.save()
        
        return response
    
    
    def delete(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        post_id = request.data.get('post_id', '')
        post = get_object_or_404(Post, pk=post_id)
        
        if request.user != post.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
        
        if request.user != post.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
    
        post.delete()
        
        return Response({
            "message": "Post delete success"
        }, status=status.HTTP_200_OK)
    
    
    def put(self, request, *args, **kwargs):
        post_id = kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        
        if request.user != post.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
        
        post.title = request.data.get('title', '')
        post.content = request.data.get('content', '')
        post.thumbnail = request.data.get('thumbnail', '')
        post.save()
        
        return Response({
            "message": "Post update success"
        }, status=status.HTTP_200_OK)

        