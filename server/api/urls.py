from django.urls import path, include


v1_patterns = [
    path('auth/', include(('auth.urls', 'auth'))),
    path('users/', include(('users.urls', 'users'))),
    path('board/', include(('boards.urls', 'boards'))),
    path('stock/', include(('stockmanage.urls', 'stock'))),
    
]


urlpatterns = [
    path('v1/', include((v1_patterns, 'v1'))),
    path('', include('swagger.urls')),
    path('manager/', include('stockmanage.urls')),
    
]
