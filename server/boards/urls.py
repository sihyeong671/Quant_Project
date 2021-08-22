from django.urls import path

from boards.apis import CategoryShowApi, CategoryManageApi, PostListApi, PostManageApi


urlpatterns = [
    path('', CategoryShowApi.as_view(), name="categories"),
    path('manage/', CategoryManageApi.as_view(), name="category manage"),
    path('<int:pk>/postlist/', PostListApi.as_view(), name="postlist"),
    path('<int:pk>/post/', PostManageApi.as_view(), name="post manage")
]
