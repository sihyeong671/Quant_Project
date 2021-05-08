import requests as rq
import pandas as pd
from io import BytesIO
import zipfile
import xml.etree.ElementTree as et
import json
import API_KEY
import os
import django

api_key = API_KEY.APIKEY
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings")
django.setup()
from quantDB.models import Company, Financial_Statements_LinkOrBasic,\
    Financial_Statements_Div, Quarter, Year, FS_Account, unique_code

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
    

def Get_Data(api_key,corp_code_,year_,quarter_,link, company):
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
    params = {'crtfc_key': api_key, 'corp_code': corp_code_, 'bsns_year': year_, 'reprt_code': quarter_, 'fs_div': link}
    res = rq.get(url, params)
    json_dict = json.loads(res.text)
    # items = ["rcept_no","reprt_code","bsns_year","sj_div","sj_nm","account_nm","account_detail","thstrm_amount"]
    # item_names = ["접수번호","보고서코드","사업연도","재무제표구분","재무제표명","계정명","계정상세","당기금액"]
    if json_dict['status'] == "000": # 정상적으로 데이터 가져옴
        BS = Financial_Statements_Div()
        BS.sj_div = "BS"
        IS = Financial_Statements_Div()
        IS.sj_div = "IS"
        CIS = Financial_Statements_Div()
        CIS.sj_div = "CIS"
        CF = Financial_Statements_Div()
        CF.sj_div = "CF"
        SCE = Financial_Statements_Div()
        SCE.sj_div = "SCE"

        for fs_lst in json_dict['list']: # 한 행씩 가져오기

            if fs_lst["sj_div"] == "BS":
                money = FS_Account()
                money.account_name = fs_lst["account_nm"]
                money.a = fs_lst["thstrm_amount"]
                money.financial_statements_div = BS

                money.save()
            elif fs_lst["sj_div"] == "IS":
                money = FS_Account()
                money.account_name = fs_lst["account_nm"]
                money.a = fs_lst["thstrm_amount"]
                money.financial_statements_div = IS
                money.save()

            elif fs_lst["sj_div"] == "CIS":
                money = FS_Account()
                money.account_name = fs_lst["account_nm"]
                money.a = fs_lst["thstrm_amount"]
                money.financial_statements_div = CIS
                money.save()

            elif fs_lst["sj_div"] == "CF":
                money = FS_Account()
                money.account_name = fs_lst["account_nm"]
                money.a = fs_lst["thstrm_amount"]
                money.financial_statements_div = CF
                money.save()

            elif fs_lst["sj_div"] == "SCE":
                money = FS_Account()
                money.account_name = fs_lst["account_nm"]
                money.a = fs_lst["thstrm_amount"]
                money.financial_statements_div = SCE
                money.save()
        BS.lb = company.year.quarter.link
        BS.save()
        IS.save()
        CIS.save()
        CF.save()
        SCE.save()
    
# financial_data(api_key,"00126380")

if __name__ == "__main__":
    # first
    # DART_data = dart_unique_key(api_key)
    # for data in DART_data:
    #     unique_code(dart_code=data[0],company_name_u=data[1],short_code=data[2],lastest_change=data[3]).save()
    #second
    linklst = ["CFS", "OFS"] # link, basic
    years = ["2015", "2016", "2017","2018","2019","2020"]
    quarters = ["11013", "11014", "11012", "11011"]
    dart_codes = unique_code.objects.all()

    for code in dart_codes:
        if code.dart_code == "00274933":
            company = Company()
            company.company_name = code.company_name_u
            for y in years:
                year = Year()
                year.bsns_year = y
                for q in quarters:
                    quarter = Quarter()
                    quarter.quarter_name = q
                    for l in linklst:
                        link = Financial_Statements_LinkOrBasic()
                        link.linkOrbasic = l
                        link.quarter = quarter
                        link.save()
                        quarter.year = year
                        quarter.save()
                        year.company = company
                        year.save()
                        # company.save()
                        Get_Data(api_key, code.dart_code, y, q, l, company)
                    



