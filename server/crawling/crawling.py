import time

from django.db import transaction

from stockmanage.models import *

from crawling.krx_crawling import *
from crawling.dart_crawling import *
from crawling.API_KEY import *

def Save_FS_Data(api_key):
    """
    상장된 기업의 Dart
    """
    linklst = ["CFS", "OFS"] # link, basic
    # years = ["2015","2016","2017","2018","2019","2020"]
    years = ["2018","2019","2020"]

    quarters = ["11013", "11014", "11012", "11011"]

    dart_codes = Dart.objects.all()
    count = 0
    for dart_data in dart_codes:
        company, flag = Company.objects.get_or_create(stock_code=dart_data.short_code)
        
        if flag:
            Save_Corp_Info(api_key, dart_data.dart_code, company)
        for y in years:
            year, flag = Year.objects.get_or_create(bs_year=int(y), company=company)
            for q in quarters:
                quarter, flag = Quarter.objects.get_or_create(qt_name=q, year=year)
                for l in linklst:
                    try:
                        FS_LoB.objects.get(lob=l, quarter=quarter)
                        check = False
                    except:
                        link = FS_LoB(lob=l, quarter=quarter)
                        check = True
                        # link, check = FS_LoB.objects.get_or_create(lob=l, quarter=quarter)
                    if check:
                        time.sleep(0.1)
                        Get_Amount_Data(api_key, dart_data.dart_code, y, q, l, link)
                        count += 1
                        if count == 100:
                            return
                        # 정정공시 따로 함수 만들기
                # ROE, ROA 계산 후 넣기


# day에 시가총액, ohlcv, per, pbr 정보 가져와서 저장
@transaction.atomic
def Save_Price():
    """
    Daily_Price 모델에 ohlcv, per, pbr 저장
    """
    corporations = Company.objects.all()
    for corp in corporations:
        # 시가총액, ohlvc, per, pbr 함수로 가져와서 저장하기
        data = Daily_Crawling("20210101", "20210401", corp.stock_code)
        time.sleep(0.1)
        
        for row in data.itertuples():
            now_date = row[0].to_pydatetime().date()
            company = Company.objects.get(corp_name=corp.corp_name, stock_code=corp.stock_code)
            
            # 현재 기업의 현재 날짜에 대한 주가가 이미 있는 경우에는 continue
            is_already_in = Daily_Price.objects.filter(
                company=company,
                date=now_date
            ).exists()
            
            if is_already_in:
                continue
            
            Daily_Data = Daily_Price(
                company=company,
                date=now_date,
                market_cap=row[1],
                open=row[2],
                high=row[3],
                low=row[4],
                close=row[5],
                volume=row[6]
            )
            # Daily_Data.per = 
            # Daily_Data.pbr = 
            Daily_Data.save()

