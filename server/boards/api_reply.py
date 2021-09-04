from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from api.mixins import ApiAuthMixin

from boards.models import Comment, Reply


class ReplyCreateApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        """
        comment_id 댓글에 새로운 대댓글을 작성한다.
        content 필수
        """
        comment_id = kwargs['comment_id']
        comment = get_object_or_404(Comment, pk=comment_id)
        
        content = request.data.get('content', '')
        
        if content == '':
            return Response({
                "message": "content required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        reply = Reply(
            creator=request.user, 
            comment=comment,
            content=content,
        )
        
        reply.save()
        
        return Response({
            "message": "Reply created success"
        }, status=status.HTTP_201_CREATED)


class ReplyManageApi(ApiAuthMixin, APIView):
    def post(self, request, *args, **kwargs):
        """
        대댓글 좋아요 기능.
        이미 좋아요를 누른 경우 취소
        """
        pk = kwargs['reply_id']
        user = request.user
        if not pk:
            return Response({
                "message": "Select a reply number"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        reply = get_object_or_404(Reply, pk=pk)
        
        if user.profile.favorite_reply.filter(pk=pk).exists():
            user.profile.favorite_reply.remove(reply)
        else:
            user.profile.favorite_reply.add(reply)
            
        return Response({
            "message": "Reply like/unlike success"
        }, status=status.HTTP_200_OK)
    
    
    def delete(self, request, *args, **kwargs):
        """
        대댓글 삭제 기능.
        """
        reply_id = kwargs['reply_id']
        reply = get_object_or_404(Reply, pk=reply_id)
        
        if request.user != reply.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
    
        reply.delete()
        
        return Response({
            "message": "Reply delete success"
        }, status=status.HTTP_204_NO_CONTENT)
    
    
    def put(self, request, *args, **kwargs):
        """
        대댓글 수정 기능.
        content
        """
        reply_id = kwargs['reply_id']
        reply = get_object_or_404(Reply, pk=reply_id)
        
        if request.user != reply.creator:
            return Response({
                "message": "You do not have permission"
            }, status=status.HTTP_403_FORBIDDEN)
        
        content = request.data.get('content', '')
        
        if content == '':
            return Response({
                "message": "content required"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        reply.content = content
        
        reply.save()
        
        return Response({
            "message": "Reply update success"
        }, status=status.HTTP_201_CREATED)
