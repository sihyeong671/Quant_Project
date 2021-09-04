from django.urls import path, include

from boards.api_category import CategoryCreateReadApi, CategoryManageApi
from boards.api_post import PostCreateApi, PostManageApi
from boards.api_comment import CommentCreateApi, CommentManageApi
from boards.api_reply import ReplyCreateApi, ReplyManageApi

# start :  ~board/

reply_urlpatterns = [
    path('reply', ReplyCreateApi.as_view(), name="reply_create"),
    path('reply/<int:reply_id>', ReplyManageApi.as_view(), name="reply_manage"),
    
]

comment_urlpatterns = [
    path('comment', CommentCreateApi.as_view(), name="comment_create"),
    path('comment/<int:comment_id>', CommentManageApi.as_view(), name="comment_manage"),
    path('comment/<int:comment_id>/', include(reply_urlpatterns)),
    
]

post_urlpatterns = [
    path('post', PostCreateApi.as_view(), name="post_create"),
    path('post/<int:post_id>', PostManageApi.as_view(), name="post_manage"),
    path('post/<int:post_id>/', include(comment_urlpatterns)),
    
]

urlpatterns = [
    path('', CategoryCreateReadApi.as_view(), name="category_create"),
    path('<int:cate_id>', CategoryManageApi.as_view(), name="category_manage"),
    path('<int:cate_id>/', include(post_urlpatterns)),
    
]
