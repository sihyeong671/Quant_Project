from django.urls import path
from .views import View_All_Data, Crawling_Data

from stockmanage.apis import CompanyNameApi, AccountApi

app_name = "stockmanage"



urlpatterns = [
    path('', View_All_Data.as_view(), name="company_list"),
    path('crawling/', Crawling_Data, name="crawling"), 
    
    path('company', CompanyNameApi.as_view(), name="company_info"),
    path('account', AccountApi.as_view()),
]
