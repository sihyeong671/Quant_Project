from django.urls import path

from . import views

app_name = "quantDB"

urlpatterns = [
    path('', views.find_state, name='find_state'),
    # path('chart/', views.show_chart, name='show_chart')
]
