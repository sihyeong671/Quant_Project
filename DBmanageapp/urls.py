from django.urls import path
from .views import View_All_Data


app_name = "DBmanageapp"

urlpatterns = [
  path('', View_All_Data.as_view(), name="company_list"), 
]