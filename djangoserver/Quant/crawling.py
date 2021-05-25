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

# pd.set_option('display.max_row', 300) # 행 갯수 늘려서 보는 옵션
# pd.set_option('display.max_column', 100) # 열 갯수 늘려서 보는 옵션 

# krx 상장회사 종목코드 가져오기
def Get_krx_corp():
    
    generate_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    generate_param = {
        'mktTpCd': '0',
        'tboxisuSrtCd_finder_listisu0_1': "전체",
        'isuSrtCd': 'ALL',
        'isuSrtCd2': 'ALL',
        # 'codeNmisuSrtCd_finder_listisu0_1':,
        # 'param1isuSrtCd_finder_listisu0_1':,
        'sortType': 'A',
        'stdIndCd': 'ALL',
        'sectTpCd': 'ALL',
        'parval': 'ALL',
        'mktcap': 'ALL',
        'acntclsMm': 'ALL',
        # 'tboxmktpartcNo_finder_designadvser0_1':,
        # 'mktpartcNo':,
        # 'mktpartcNo2':,
        # 'codeNmmktpartcNo_finder_designadvser0_1':,
        # 'param1mktpartcNo_finder_designadvser0_1':,
        'condListShrs': '1',
        # 'listshrs':,
        # 'listshrs2':,
        'condCap': '1',
        # 'cap':,
        # 'cap2':,
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT03402'
    }
    headers = {'User-Agent': API_KEY.USERAGENT}
    generate_res = rq.post(generate_url, generate_param, headers = headers)
    code = generate_res.content

    download_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
    download_param = {'code': code}

    download_res = rq.post(download_url, download_param, headers = headers)

    corp = pd.read_excel(BytesIO(download_res.content), dtype={'종목코드': str})
    
    return corp['종목코드']

def Dart_unique_key(api_key):
    # dart에서 고유번호 가져오기
    items = ["corp_code", "corp_name", "stock_code", "modify_date"]  # OpenApi에서 주는 정보
    # item_names = ["고유번호", "회사명", "종목코드", "최종변경일자"]
    url = "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={}".format(api_key)
    resp = rq.get(url)
    zfile = zipfile.ZipFile(BytesIO(resp.content))
    tree = zfile.open(zfile.namelist()[0])  # 압축파일 내의 CORPCODE.xml 열기
    # xml 파일 파싱하기
    root = et.fromstring(tree.read().decode('utf-8'))
    data = []
    krx_short_code = list(Get_krx_corp())
    for child in root:      
        # 상장회사만 가져오기
        dart_short_code = child.find('stock_code').text.strip()
        if dart_short_code in krx_short_code:
            data.append([])
            for item in items:
                data[-1].append(child.find(item).text)
    return data

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
        print(corp_code, year_,quarter_, link_)
        print(json_dict['status'])

# data = Company.objects.all()
# data.delete()

if __name__ == "__main__":
    # k = "first"
    k = "second"

    if k == "first":
        dart_data = Dart_unique_key(api_key)
        for data in dart_data:
            Dart(dart_code=data[0],company_name_dart=data[1],short_code=data[2],recent_modify=data[3]).save()
    elif k == "second":
        linklst = ["CFS", "OFS"] # link, basic
        years = ["2020"]
        # years = ["2015", "2016", "2017","2018","2019","2020"]

        # 기업 데이터 이미 있는지 확인 하는 코드 추가
        # api 받아오는거 없으면 pass
        quarters = ["11013", "11014", "11012", "11011"]

        dart_codes = Dart.objects.all()

        count = 1
        # 상폐된거 인식해줘야함
        # 013 => 데이터 없음
        for code in dart_codes:
            company = Company()
            company.company_name = code.company_name_dart
            company.save()
            for y in years:
                year = Year()
                year.bs_year = int(y)
                year.company = company
                year.save()
                time.sleep(8)
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
                        
                        if count == 10000:
                            exit()
                            

