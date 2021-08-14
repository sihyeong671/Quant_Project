import time
from datetime import date, datetime

from .models import *
from .dart_crawling import *
from .krx_crawling import *
from .API_KEY import APIKEY

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

api_key = APIKEY
# data 존재여부 확인 함수
def make_company_obje(dartdata):
    # 코스피, 코스닥
    # 결산월
    cmpname = dartdata.company_name_dart
    cmpcode = dartdata.short_code
    # dart에서 가져온 company이름과 동일한 이름을 가진 company 객체가 있다면 그대로 반환
    try:
        company = Company.objects.get(company_name=cmpname)
        return company
    except:
        company = Company(company_name = cmpname, short_code = cmpcode)
        company.save()
        return company

def make_year_obje(comp:Company, year:str):
    # company 객체를 가져와서 해당 company 객체에 인자로 받은 year가 존재하면 그대로 반환

    for y in comp.year.all():
        if y.bs_year == int(year):
            return y

    y = Year(company=comp, bs_year=int(year))
    y.save()
    return y

def make_quarter_obje(year:Year, quarter:str):
    # year 객체를 가져와서 해당 year 객체에 인자로 받은 quarter가 존재하면 그대로 반환
    for q in year.quarter.all():
        if q.qt_name == quarter:
            return q

    q = Quarter(year=year, qt_name=quarter)
    q.save()
    return q
    
def make_islink_obje(quarter:Quarter, islink:str):
    # year 객체를 가져와서 해당 year 객체에 인자로 받은 quarter가 존재하면 그대로 반환
    for l in quarter.fs_lob.all():
        if l.lob == islink:
            return l, False

    l = FS_LoB(quarter=quarter, lob=islink, exist=0)
    l.save()
    return l, True

# 고유번호, 단축코드, 기업명, 최근 수정 날짜 저장
def Save_Dart_Data(api_key):
    dart_data = Dart_Unique_Key(api_key)
    for data in dart_data:
        dart = Dart(dart_code=data[0],company_name_dart=data[1],short_code=data[2],recent_modify=data[3])
        dart.save()

# 재무제표 데이터 저장
def Save_FS_Data(api_key):
    linklst = ["CFS", "OFS"] # link, basic
    # years = ["2015","2016","2017","2018","2019","2020"]
    years = ["2018","2019","2020"]

    quarters = ["11013", "11014", "11012", "11011"]

    dart_codes = Dart.objects.all()
    count = 0
    
    for dart_data in dart_codes:
        company = make_company_obje(dart_data)
        print(company.company_name)
        for y in years:
            year = make_year_obje(company, y)
            for q in quarters:
                quarter = make_quarter_obje(year, q)
                for l in linklst:
                    link, check = make_islink_obje(quarter, l)
                    if check:
                        count += 1
                        time.sleep(0.1)
                        if count == 100:
                            return
                        Get_Amount_Data(api_key, dart_data.dart_code, y, q, l, link)
                        # 정정공시 따로 함수 만들기
                        

# day에 시가총액, ohlcv, per, pbr 정보 가져와서 저장
def Save_Price():
    corporations = Company.objects.all()
    for corp in corporations:
         # 시가총액, ohlvc, per, pbr 함수로 가져와서 저장하기
        data = Daily_Crawling("20200101", "20210101", corp.short_code)
        for row in data.itertuples():
            Daily_Data = Daily_Price()
            Daily_Data.company = Company(company_name = corp.company_name, short_code = corp.short_code)
            Daily_Data.date = row[0].to_pydatetime().date()
            Daily_Data.market_gap = row[1]
            Daily_Data.open = row[2]
            Daily_Data.high = row[3]
            Daily_Data.low = row[4]
            Daily_Data.close = row[5]
            Daily_Data.per = row[6]
            Daily_Data.pbr = row[7]
            Daily_Data.save()


Save_Dart_Data(api_key)
time.sleep(1)
Save_FS_Data(api_key)
time.sleep(1)
Save_Price()
# 매일 업데이트 하는 함수


    

