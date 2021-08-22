from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from api.mixins import PublicApiMixin, ApiAuthMixin

from boards.serializers import CategorySerializer, PostSerializer
from boards.models import Category, Post, Comment, Reply


class CategoryShowApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class CategoryManageApi(ApiAuthMixin, APIView):
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
    
    def delete(self, request, *args, **kwargs):
        category = Category.objects.get(pk=request.data.get('id', ''))
        
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
            "message": "Success delete"
        }, status=status.HTTP_200_OK)


class PostListApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        category_id = kwargs['pk']
        
        if not category_id:
            return Response({
                "message": "Select a board type"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        category = Category.objects.get(pk=category_id)
        postlist = Post.objects.filter(category=category)
        
        return Response(
            PostSerializer(
                postlist, many=True).data,
                status=status.HTTP_200_OK)


class PostManageApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        category = get_object_or_404(Category, pk=kwargs['pk'])
        
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
    
    
    def delete(self, request, *args, **kwargs):
        category = get_object_or_404(Category, pk=request.data.get('pk', ''))
        
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
            "message": "Delete Success!"
        }, status=status.HTTP_200_OK)
