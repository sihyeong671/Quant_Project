from django.urls import path

from logapp.apis import GetLogApi

urlpatterns = [
    path('getlog', GetLogApi.as_view()),
    
]
