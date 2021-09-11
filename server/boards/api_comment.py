from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from api.mixins import ApiAuthMixin

from boards.models import Post, Comment


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
        
        if user.profile.favorite_comment.filter(pk=pk).exists():
            user.profile.favorite_comment.remove(comment)
        else:
            user.profile.favorite_comment.add(comment)
            
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
            "message": "Comment delete success"
        }, status=status.HTTP_204_NO_CONTENT)
    
    
    def put(self, request, *args, **kwargs):
        """
        댓글 수정 기능.
        content
        """
        comment_id = kwargs['comment_id']
        comment = get_object_or_404(Comment, pk=comment_id)
        
        if request.user != comment.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
        
        content = request.data.get('content', '')
        
        if content == '':
            return Response({
                "message": "content required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        comment.content = content
        
        comment.save()
        
        return Response({
            "message": "Comment update success"
        }, status=status.HTTP_201_CREATED)
        
