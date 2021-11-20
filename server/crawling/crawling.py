import time
import math

from django.db import transaction
from django.db.models import Q

from stockmanage.models import *

from crawling.krx_crawling import *
from crawling.dart_crawling import *
from crawling.API_KEY import *


QUARTER = {
        1: "11013",
        2: "11012",
        3: "11014",
        4: "11011",
    }


def Save_FS_Data(api_key):
    """
    상장된 기업의 Dart
    """
    linklst = ["CFS", "OFS"] # link, basic
    years = ["2015","2016","2017","2018","2019","2020","2021"]
    # years = ["2018","2019","2020", "2021"]

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
                        time.sleep(0.5)
                        Get_Amount_Data(api_key, dart_data.dart_code, y, q, l, link)
                        count += 1
                        if count == 1000:
                            return
                        # 정정공시 따로 함수 만들기
                # ROE, ROA 계산 후 넣기


def get_per_pbr(queryset, condition, market_cap, now_quarter:str, prev_quarter, now_year:int, prev_year, lob):
    if lob == "CFS":
        condition.add(Q(lob="CFS"), Q.AND)
    else:
        condition.add(Q(lob="OFS"), Q.AND)
        
    query = queryset.filter(
        condition,
        quarter__year__bs_year=now_year,
        quarter__qt_name=now_quarter
    )
    
    if not query.exists():
        query = queryset.filter(
            condition,
            quarter__year__bs_year=prev_year,
            quarter__qt_name=prev_quarter
        )
        
    per = 0
    pbr = 0
    if query.exists():
        lob = query.first()
        per = market_cap / lob.net_income
        pbr = market_cap / lob.total_capital
    
    return per, pbr
    

def Find_PBR_PER(now_quarter:str, prev_quarter, now_year:int, prev_year, company, market_cap):
    condition = Q(quarter__year__company=company)
    condition.add(Q(exist=1), Q.AND)
    queryset = FS_LoB.objects.\
        select_related(
            'quarter',
            'quarter__year',
            'quarter__year__company'
        )
        
    cfs_per=cfs_pbr=ofs_per=ofs_pbr=0
    
    cfs_per, cfs_pbr = get_per_pbr(queryset, condition, market_cap, now_quarter, prev_quarter, now_year, prev_year, "CFS")
    ofs_per, ofs_pbr = get_per_pbr(queryset, condition, market_cap, now_quarter, prev_quarter, now_year, prev_year, "OFS")
    
    return cfs_per, cfs_pbr, ofs_per, ofs_pbr
    

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
            strn_date = "".join(str(now_date).split('-'))
            now_year = int(strn_date[0:4])
            now_quarter = QUARTER[math.ceil(int(strn_date[4:6]) / 3.0)]
            if math.ceil(int(strn_date[4:6]) / 3.0) == 1:
                prev_quarter = QUARTER[4]
                prev_year = now_year - 1
            else:
                prev_quarter = QUARTER[(math.ceil(int(strn_date[4:6]) / 3.0))- 1]
                prev_year = now_year
            company = Company.objects.get(corp_name=corp.corp_name, stock_code=corp.stock_code)
            cfs_per, cfs_pbr, ofs_per, ofs_pbr = \
            Find_PBR_PER(now_quarter, prev_quarter, now_year, prev_year, company, row[1])
            
            
            # 현재 기업의 현재 날짜에 대한 주가가 이미 있는 경우에는 continue
            already = Daily_Price.objects.filter(
                company=company,
                date=now_date
            )
            
            if already.exists():
                already.company=company
                already.date=now_date,
                already.market_cap=row[1],
                already.open=row[2],
                already.high=row[3],
                already.low=row[4],
                already.close=row[5],
                already.volume=row[6],
                already.cfs_per=cfs_per,
                already.cfs_pbr=cfs_pbr,
                already.ofs_per=ofs_per,
                already.ofs_pbr=ofs_pbr
                
                already.save()
            else:
                Daily_Data = Daily_Price(
                    company=company,
                    date=now_date,
                    market_cap=row[1],
                    open=row[2],
                    high=row[3],
                    low=row[4],
                    close=row[5],
                    volume=row[6],
                    cfs_per=cfs_per,
                    cfs_pbr=cfs_pbr,
                    ofs_per=ofs_per,
                    ofs_pbr=ofs_pbr
                )
                Daily_Data.save()

