from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from api.mixins import ApiAuthMixin, SuperUserMixin

from boards.serializers import CategorySerializer, PostListSerializer
from boards.models import Category, Post


class CategoryCreateReadApi(SuperUserMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        현재 생성되어있는 카테고리(게시판 종류)를 모두 보여준다.
        """
        serializer = CategorySerializer(Category.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        카테고리를 새로 만든다. title 필수
        """
        title = request.data.get('title', '')
        
        if title == '':
            return Response({
            "message": "Title required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if Category.objects.filter(title=title).first():
            return Response({
            "message": "Title duplicated"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        category = Category(
            creator=request.user, 
            title=title,
            is_anonymous=request.data.get('anonymous', False),
            top_fixed=request.data.get('fixed', False),
        )
        
        category.save()
        
        return Response({
            "message": "Category created success"
        }, status=status.HTTP_201_CREATED)


class CategoryManageApi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        cate_id에 맞는 게시판의 글을 모두 보여준다.
        """
        pk = kwargs['cate_id']
        
        if not pk:
            return Response({
                "message": "Select a board type"
            }, status=status.HTTP_400_BAD_REQUEST)
            
        category = get_object_or_404(Category, pk=pk)
        postlist = Post.objects.filter(category=category)
        
        serializer = PostListSerializer(postlist, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request, *args, **kwargs):
        """
        cate_id에 맞는 게시판을 즐겨찾기한다.
        이미 즐겨찾기가 되어있는경우 취소한다.
        """
        pk = kwargs['cate_id']
        user = request.user
        if not pk:
            return Response({
                "message": "Select a board type"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        category = get_object_or_404(Category, pk=pk)
        
        if user.profile.favorite_category.filter(pk=pk).exists():
            user.profile.favorite_category.remove(category)
        else:
            user.profile.favorite_category.add(category)
            
        return Response({
            "message": "Category like/unlike success"
        }, status=status.HTTP_200_OK)
        
        
    def delete(self, request, *args, **kwargs):
        """
        cate_id에 맞는 카테고리를 삭제한다. 
        해당 카테고리에 글이 작성된 경우 삭제 불가능.
        """
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
        }, status=status.HTTP_204_NO_CONTENT)
    