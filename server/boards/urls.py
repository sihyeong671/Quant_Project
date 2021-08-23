from django.urls import path, include

from boards.apis import CategoryCreateReadApi, \
    CategoryDeleteAndPostListApi, PostManageAPi, PostCreateApi \


# start :  ~board/
post_urlpatterns = [
    path('post', PostCreateApi.as_view(), name="post_create"),
    path('post/<int:post_id>', PostManageAPi.as_view(), name="post_manage"),
    
]

urlpatterns = [
    path('', CategoryCreateReadApi.as_view(), name="category_cr"),
    path('<int:cate_id>', CategoryDeleteAndPostListApi.as_view(), 
         name="category_delete_post_list"),
    
    path('<int:cate_id>/', include(post_urlpatterns)),
]
