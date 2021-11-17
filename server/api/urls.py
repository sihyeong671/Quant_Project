from django.urls import path, include


v1_patterns = [
    path('auth/', include(('auth.urls', 'auth'))),
    path('users/', include(('users.urls', 'users'))),
    path('board/', include(('boards.urls', 'boards'))),
    path('stock/', include(('stockmanage.urls', 'stock'))),
    path('log/', include(('logapp.urls', 'log'))),
    
]

def trigger_error(request):
    division_by_zero = 1 / 0
    
urlpatterns = [
    path('v1/', include((v1_patterns, 'v1'))),
    path('', include('swagger.urls')),
    path('sentry-debug/', trigger_error),
    
]
