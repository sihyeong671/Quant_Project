from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404

from api.mixins import PublicApiMixin, ApiAuthMixin

from boards.serializers import CategorySerializer, PostSerializer,\
    PostDetailSerializer
from boards.models import Category, Post, Comment, Reply


class CategoryCreateReadApi(ApiAuthMixin, APIView):
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
        if request.data.get('title', '') == '':
            return Response({
            "message": "Title required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        category = Category(
            creator=request.user, 
            title=request.data.get('title'),
            is_anonymous=request.data.get('anonymous', False)
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
            
        category = Category.objects.get(pk=pk)
        postlist = Post.objects.filter(category=category)
        
        serializer = PostSerializer(postlist, many=True)
        
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
        
        if user.favorite_category.filter(pk=pk).exists():
            category.favorite.remove(user)
        else:
            category.favorite.add(user)
            
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
        }, status=status.HTTP_200_OK)
        
    
class PostCreateApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        """
        cate_id 게시판에 새로운 글을 작성한다.
        title, content 필수
        """
        cate_id = kwargs['cate_id']
        category = get_object_or_404(Category, pk=cate_id)
        
        title = request.data.get('title', '')
        content = request.data.get('content', '')
        
        if title == '' or content == '':
            return Response({
                "message": "title/content required"
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


class PostManageApi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        post_id에 맞는 글을 불러온다.
        쿠키를 사용한 조회수 체크
        유저당 10분에 한 번씩 해당 글의 조회수를 올릴 수 있다.
        """
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
    
    def post(self, request, *args, **kwargs):
        """
        게시글 좋아요 기능.
        이미 좋아요를 누른 경우 취소
        """
        pk = kwargs['post_id']
        user = request.user
        if not pk:
            return Response({
                "message": "Select a post number"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        post = get_object_or_404(Post, pk=pk)
        
        if user.favorite_post.filter(pk=pk).exists():
            post.favorite.remove(user)
        else:
            post.favorite.add(user)
            
        return Response({
            "message": "Post like/unlike success"
        }, status=status.HTTP_200_OK)
    
    
    def delete(self, request, *args, **kwargs):
        """
        글 삭제 기능.
        """
        post_id = kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        
        if request.user != post.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
    
        post.delete()
        
        return Response({
            "message": "Post delete success"
        }, status=status.HTTP_200_OK)
    
    
    def put(self, request, *args, **kwargs):
        """
        글 수정 기능.
        title, content, thumbnail 
        """
        post_id = kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        
        if request.user != post.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
        
        title = request.data.get('title', '')
        content = request.data.get('content', '')
        
        if title == '' or content == '':
            return Response({
                "message": "title required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        post.title = title
        post.content = content
        post.thumbnail = request.data.get('thumbnail', '')
        
        post.save()
        
        return Response({
            "message": "Post update success"
        }, status=status.HTTP_200_OK)


class CommentCreateApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        """
        post_id 글에 새로운 댓글을 작성한다.
        content 필수
        """
        post_id = kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        
        content = request.data.get('content', '')
        
        if content == '':
            return Response({
                "message": "content required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        comment = Comment(
            creator=request.user, 
            post=post,
            content=content,
        )
        
        comment.save()
        
        return Response({
            "message": "Comment created success"
        }, status=status.HTTP_201_CREATED)


class CommentManageApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        """
        댓글 좋아요 기능.
        이미 좋아요를 누른 경우 취소
        """
        pk = kwargs['comment_id']
        user = request.user
        if not pk:
            return Response({
                "message": "Select a comment number"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        comment = get_object_or_404(Comment, pk=pk)
        
        if user.favorite_comment.filter(pk=pk).exists():
            comment.favorite.remove(user)
        else:
            comment.favorite.add(user)
            
        return Response({
            "message": "Comment like/unlike success"
        }, status=status.HTTP_200_OK)
    
    
    def delete(self, request, *args, **kwargs):
        """
        댓글 삭제 기능.
        """
        comment_id = kwargs['comment_id']
        comment = get_object_or_404(Comment, pk=comment_id)
        
        if request.user != comment.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
    
        comment.delete()
        
        return Response({
            "message": "Post delete success"
        }, status=status.HTTP_200_OK)
    
    
    def put(self, request, *args, **kwargs):
        """
        댓글 수정 기능.
        title, content, thumbnail 
        """
        comment_id = kwargs['comment_id']
        comment = get_object_or_404(Post, pk=comment_id)
        
        if request.user != comment.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
        
        content = request.data.get('title', '')
        
        if content == '':
            return Response({
                "message": "title required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        comment.content = content
        
        comment.save()
        
        return Response({
            "message": "Comment update success"
        }, status=status.HTTP_200_OK)