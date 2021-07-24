import json
import os
import django
import time
from datetime import date
from pykrx import stock
from django.db.models import Q

api_key = API_KEY.APIKEY
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")
django.setup()

from quantDB.models import Dart
from quantDB.models import Company, FS_LoB,\
    FS_Div, Quarter, Year, FS_Account, Dart, Corpdata

pd.set_option('display.max_row', 300) # 행 갯수 늘려서 보는 옵션
pd.set_option('display.max_column', 100) # 열 갯수 늘려서 보는 옵션 

# def Daily_Crawling():
#     today = date.today().isoformat().replace('-', '')
#     df_market_cap = stock.get_market_cap_by_ticker(today, market="ALL") # index -> ticker == shortcode
#     df_p2 = stock.get_market_fundamental_by_ticker(today, market="ALL")
#     corpdata = Corpdata()

#     for idx in range(len(df_market_cap)):
#         corpdata.company = Company.objects.filter(short_code=df_market_cap.index[idx])
#         corpdata.market_cap = df_market_cap["시가총액"][idx]

#     for idx in range(len(df_p2)):
#         corpdata.company = Company.objects.filter(short_code=df_p2.index[idx])
#         corpdata.pbr = df_p2["PBR"][idx]
#         corpdata.per = df_p2["PER"][idx]
#     corpdata.save()

# krx 상장회사 종목코드 가져오기




def Get_Data(api_key,corp_code_,year_,quarter_,link_, link):
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
    params = {'crtfc_key': api_key, 'corp_code': corp_code_, 'bsns_year': year_, 'reprt_code': quarter_, 'fs_div': link_}
    res = rq.get(url, params)
    json_dict = json.loads(res.text)
    if json_dict['status'] == "000": # 정상적으로 데이터 가져옴
        BS = FS_Div()
        BS.sj_div = "BS"
        IS = FS_Div()
        IS.sj_div = "IS"
        CIS = FS_Div()
        CIS.sj_div = "CIS"
        CF = FS_Div()
        CF.sj_div = "CF"
        SCE = FS_Div()
        SCE.sj_div = "SCE"

        BS.lob = link
        IS.lob = link
        CIS.lob = link
        CF.lob = link
        SCE.lob = link

        BS.save()
        IS.save()
        CIS.save()
        CF.save()
        SCE.save()

        for fs_lst in json_dict['list']: # 한 행씩 가져오기
            money = FS_Account()
            money.account_name = fs_lst["account_nm"]
            money.account_detail = fs_lst["account_detail"]
            if fs_lst["thstrm_amount"] == '':
                money.account_amount = 0
            else:
                money.account_amount = fs_lst["thstrm_amount"]

            if fs_lst["sj_div"] == "BS":
                money.fs_div = BS

            elif fs_lst["sj_div"] == "IS":
                money.fs_div = IS

            elif fs_lst["sj_div"] == "CIS":
                money.fs_div = CIS

            elif fs_lst["sj_div"] == "CF":
                money.fs_div = CF

            elif fs_lst["sj_div"] == "SCE":
                money.fs_div = SCE

            money.save()
    else:
        print('dart error')
        print(corp_code_, year_,quarter_, link_)
        print(json_dict['status'])
        print("\n\n")

## delete data ##
# data = Company.objects.all()
# data.delete()

def make_company_obje(dartcode):
    cmpname = dartcode.company_name_dart
    cmpcode = dartcode.short_code
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
    for y in comp.year_set.all():
        if y.bs_year == int(year):
            return y

    y = Year(company=comp, bs_year=int(year))
    y.save()
    return y

def make_quarter_obje(year:Year, quarter:str):
    # year 객체를 가져와서 해당 year 객체에 인자로 받은 quarter가 존재하면 그대로 반환
    for q in year.quarter_set.all():
        if q.qt_name == quarter:
            return q

    q = Quarter(year=year, qt_name=quarter)
    q.save()
    return q
    
def make_islink_obje(quarter:Quarter, islink:str):
    # year 객체를 가져와서 해당 year 객체에 인자로 받은 quarter가 존재하면 그대로 반환
    for l in quarter.fs_lob_set.all():
        if l.lob == islink:
            return l, False

    l = FS_LoB(quarter=quarter, lob=islink)
    l.save()
    return l, True

if __name__ == "__main__":
    # k = "first"
    k = "second"
    # k = "third"

    if k == "first":
        dart_data = Dart_Unique_Key(api_key)
        for data in dart_data:
            Dart(dart_code=data[0],company_name_dart=data[1],short_code=data[2],recent_modify=data[3]).save()
    elif k == "second":
        linklst = ["CFS", "OFS"] # link, basic
        years = ["2015","2016","2017","2018","2019","2020"]
        # 기업 데이터 이미 있는지 확인 하는 코드 추가
        quarters = ["11013", "11014", "11012", "11011"]

        dart_codes = Dart.objects.all()
        count = 1
        # 013 => 데이터 없음
        company_list = Company.objects.all()
        for code in dart_codes:
            company = make_company_obje(code)
            for y in years:
                year = make_year_obje(company, int(y))
                for q in quarters:
                    quarter = make_quarter_obje(year, q)
                    for l in linklst:
                        link, check = make_islink_obje(quarter, l)
                        if check:
                            count += 1
                            if count % 1000 == 0:
                                time.sleep(5)
                            elif count == 10000:
                                exit()
                            Get_Data(api_key, code.dart_code, y, q, l, link)
                            # 정정공시 따로 함수 만들기
                            
                        
    elif k =="third":
        Daily_Crawling()
                            

