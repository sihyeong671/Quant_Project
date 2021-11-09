from django.urls import path
# from .views import View_All_Data, Crawling_Data

from stockmanage.apis import CompanyNameApi, AccountSearchApi, \
    DailyPriceApi, Crawling_Data, CustomBSApi, Crawling_Dart

app_name = "stockmanage"



urlpatterns = [
    # path('', View_All_Data.as_view(), name="company_list"),
    path('crawlingdarts', Crawling_Dart.as_view(), name="crawlingdart"),
    path('crawlingfs', Crawling_Data.as_view(), name="crawling"),
    path('company', CompanyNameApi.as_view(), name="company_info"),
    path('account', AccountSearchApi.as_view(), name="account_search"),
    path('daily', DailyPriceApi.as_view(), name="daily_price"),
    path('custombs', CustomBSApi.as_view(), name="make_custombs"),
    
]
