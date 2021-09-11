from django.urls import path
from .views import View_All_Data, Crawling_Data

<<<<<<< HEAD
from stockmanage.apis import CompanyNameApi, AccountApi
=======
from stockmanage.apis import CompanyNameApi, DailyPriceApi
>>>>>>> a428c6cf323051997d2653b6ed4c8cb7752c674a

app_name = "stockmanage"



urlpatterns = [
    path('', View_All_Data.as_view(), name="company_list"),
    path('crawling/', Crawling_Data, name="crawling"), 
    
    path('company', CompanyNameApi.as_view(), name="company_info"),
<<<<<<< HEAD
    path('account', AccountApi.as_view()),
=======
    path('daily/<str:code>', DailyPriceApi.as_view(), name="daily_price"),
    
>>>>>>> a428c6cf323051997d2653b6ed4c8cb7752c674a
]
