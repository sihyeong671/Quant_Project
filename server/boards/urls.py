from django.urls import path, include

from boards.apis import CategoryCreateReadApi, \
    CategoryManageApi, PostManageApi, PostCreateApi, \
    CommentCreateApi, CommentManageApi


# start :  ~board/

reply_urlpatterns = [
    # path('reply',)
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
    path('', CategoryCreateReadApi.as_view(), name="category_cr"),
    path('<int:cate_id>', CategoryManageApi.as_view(), name="category_manage"),
    path('<int:cate_id>/', include(post_urlpatterns)),
    
]
