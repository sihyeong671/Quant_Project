import time

from stockmanage.models import *

from crawling.krx_crawling import *
from crawling.dart_crawling import *
from crawling.API_KEY import *





def Save_FS_Data(api_key):
    linklst = ["CFS", "OFS"] # link, basic
    # years = ["2015","2016","2017","2018","2019","2020"]
    years = ["2018","2019","2020"]

    quarters = ["11013", "11014", "11012", "11011"]

    dart_codes = Dart.objects.all()
    count = 0
    # 함수만들어서 기업개황 정보 집어넣기
    for dart_data in dart_codes:
        company, flag = Company.objects.get_or_create(stock_code=dart_data.short_code)
        
        if flag:
            Save_Corp_Info(api_key, dart_data.dart_code, company)
        for y in years:
            year, flag = Year.objects.get_or_create(bs_year=int(y), company=company)
            for q in quarters:
                quarter, flag = Quarter.objects.get_or_create(qt_name=q, year=year)
                for l in linklst:
                    link, check = FS_LoB.objects.get_or_create(lob=l, quarter=quarter)
                    if check:
                        count += 1
                        time.sleep(0.1)
                        if count == 100:
                            return
                        Get_Amount_Data(api_key, dart_data.dart_code, y, q, l, link)
                        # 정정공시 따로 함수 만들기
                # ROE, ROA 계산 후 넣기

# day에 시가총액, ohlcv, per, pbr 정보 가져와서 저장
def Save_Price():
    corporations = Company.objects.all()
    for corp in corporations:
        # 시가총액, ohlvc, per, pbr 함수로 가져와서 저장하기
        data = Daily_Crawling("20201201", "20210101", corp.short_code)
        time.sleep(1)
        for row in data.itertuples():
            Daily_Data = Daily_Price()
            Daily_Data.company = Company.objects.get(corp_name = corp.corp_name, short_code = corp.short_code)
            Daily_Data.date = row[0].to_pydatetime().date()
            Daily_Data.market_gap = row[1]
            Daily_Data.open = row[2]
            Daily_Data.high = row[3]
            Daily_Data.low = row[4]
            Daily_Data.close = row[5]
            Daily_Data.volume = row[6]
            # Daily_Data.per = 
            # Daily_Data.pbr = 
            Daily_Data.save()


# day에 시가총액, ohlcv, per, pbr 정보 가져와서 저장

def Save_Price():
    corporations = Company.objects.all()
    for corp in corporations:
        # 시가총액, ohlvc, per, pbr 함수로 가져와서 저장하기
        data = Daily_Crawling("20201201", "20210101", corp.short_code)
        time.sleep(1)
        # 직전 분기의 재무제표를 가져와 PER, PBR산출
        for row in data.itertuples():
            Daily_Data = Daily_Price()
            Daily_Data.company = Company.objects.get(company_name = corp.company_name, short_code = corp.short_code)
            Daily_Data.date = row[0].to_pydatetime().date()
            Daily_Data.market_gap = row[1]
            Daily_Data.open = row[2]
            Daily_Data.high = row[3]
            Daily_Data.low = row[4]
            Daily_Data.close = row[5]
            Daily_Data.volume = row[6]
            # Daily_Data.per = 
            # Daily_Data.pbr = 
            Daily_Data.save()
