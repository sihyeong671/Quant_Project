from django.urls import path, include

from stockmanage.apis import CompanyNameApi, AccountSearchApi, \
    DailyPriceApi, FSChartApi, CustomBSApi, RankApi
from stockmanage.crawlingapis import Crawling_FSData, Crawling_Dart, Crawling_DailyPrice

app_name = "stockmanage"


# url starts with : /api/v1/stock/...

basic_patterns = [
    path('company', CompanyNameApi.as_view(), name="company_info"),
    path('account', AccountSearchApi.as_view(), name="account_search"),
    path('custombs', CustomBSApi.as_view(), name="make_custombs"),
    path('rank', RankApi.as_view(), name="rank"),
    
]

chart_patterns = [
    path('daily', DailyPriceApi.as_view(), name="daily_price"),
    path('lob', FSChartApi.as_view(), name="lob"),
    
]

crawling_patterns = [
    path('dart', Crawling_Dart.as_view(), name="crawlingdarts"),
    path('fs', Crawling_FSData.as_view(), name="crawlingfs"),
    path('daily', Crawling_DailyPrice.as_view(), name="crawlingdaily"),
]

urlpatterns = [
    path('crawling/', include((crawling_patterns, 'crawling'))),
    path('chart/', include((chart_patterns, 'chart'))),
    path('', include((basic_patterns, 'basic'))),
    
]
