import requests as rq
import pandas as pd
from io import BytesIO
import zipfile
import xml.etree.ElementTree as et
import json
import API_KEY
import os
import django
import time

api_key = API_KEY.APIKEY
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")
django.setup()

from quantDB.models import Dart
from quantDB.models import Company, FS_LoB,\
    FS_Div, Quarter, Year, FS_Account, Dart
from django.db.models import Q

# pd.set_option('display.max_row', 300) # 행 갯수 늘려서 보는 옵션
# pd.set_option('display.max_column', 100) # 열 갯수 늘려서 보는 옵션 

def dart_unique_key(api_key):
    # dart에서 고유번호 가져오기
    items = ["corp_code", "corp_name", "stock_code", "modify_date"]  # OpenApi에서 주는 정보
    # item_names = ["고유번호", "회사명", "종목코드", "최종변경일자"]
    url = "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={}".format(api_key)
    resp = rq.get(url)
    zfile = zipfile.ZipFile(BytesIO(resp.content))
    tree = zfile.open(zfile.namelist()[0])  # 압축파일 내의 CORPCODE.xml 열기
    # xml 파일 파싱하기
    root = et.fromstring(tree.read().decode('utf-8'))
    # print(root)
    data = []
    for child in root:
        # 상장회사만 가져오기
        if len(child.find('stock_code').text.strip()) > 1:  # stock_code 없는 기업 제외
            data.append([])
            for item in items:
                data[-1].append(child.find(item).text)
    return data

def Get_Data(api_key,corp_code_,year_,quarter_,link_, link):
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
    params = {'crtfc_key': api_key, 'corp_code': corp_code_, 'bsns_year': year_, 'reprt_code': quarter_, 'fs_div': link_}
    res = rq.get(url, params)
    json_dict = json.loads(res.text)
    # items = ["rcept_no","reprt_code","bsns_year","sj_div","sj_nm","account_nm","account_detail","thstrm_amount"]
    # item_names = ["접수번호","보고서코드","사업연도","재무제표구분","재무제표명","계정명","계정상세","당기금액"]
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


# financial_data(api_key,"00126380")

def make_company_obje(dartcode):
    cmpname = dartcode.company_name_dart
    company = Company.objects.get(company_name=cmpname)
    
    # dart에서 가져온 company이름과 동일한 이름을 가진 company 객체가 있다면 그대로 반환
    if company:
        return company
    else:
        company = Company(company_name = cmpname)
        company.save()
        return company


def make_year_obje(comp:Company, year:str):
    # company 객체를 가져와서 해당 company 객체에 인자로 받은 year가 존재하면 그대로 반환
    for y in comp.year_set.all():
        if y.bs_year == int(year):
            return y

    y = Year(company=comp, bs_year=int(year))
    return y


def make_quarter_obje(year:Year, quarter:str):
    # year 객체를 가져와서 해당 year 객체에 인자로 받은 quarter가 존재하면 그대로 반환
    for q in year.quarter_set.all():
        if q.qt_name == quarter:
            return q

    q = Quarter(year=year, qt_name=quarter)
    return q
    
def make_islink_obje(quarter:Quarter, islink:str):
    # year 객체를 가져와서 해당 year 객체에 인자로 받은 quarter가 존재하면 그대로 반환
    for l in quarter.fs_lob_set.all():
        if l.lob == islink:
            return l

    l = FS_LoB(quarter=quarter, lob=islink)
    return l

if __name__ == "__main__":
    # k = "first"
    k = "second"

    if k == "first":
        DART_data = dart_unique_key(api_key)
        for data in DART_data:
            Dart(dart_code=data[0],company_name_dart=data[1],short_code=data[2],recent_modify =data[3]).save()
    elif k == "second":
        linklst = ["CFS", "OFS"] # link, basic
        years = ["2019","2020"]
        # years = ["2015", "2016", "2017","2018","2019","2020"]

        quarters = ["11013", "11014", "11012", "11011"]
        dart_codes = Dart.objects.all()
        count = 0
        for code in dart_codes:
            if code.dart_code == "00274933":
                company = Company()
                company.company_name = code.company_name_dart
                company.save()
                for y in years:
                    year = Year()
                    year.bs_year = int(y)
                    year.company = company
                    year.save()
                    for q in quarters:
                        quarter = Quarter()
                        quarter.qt_name = q
                        quarter.year = year
                        quarter.save()
                        for l in linklst:
                            link = FS_LoB()
                            link.lob = l
                            link.quarter = quarter
                            link.save()
                            count += 1 
                            Get_Data(api_key, code.dart_code, y, q, l, link)
                            if count == 2:
                                print('success')
                                exit()
