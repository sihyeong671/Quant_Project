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
    
def make_financial_state(api_key,company_name_,corp_code_,year_,quarter_,link): # link/basic

    url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
    params = {'crtfc_key': api_key, 'corp_code': corp_code, 'bsns_year': year_, 'reprt_code': quarter_, 'fs_div': link}
    res = rq.get(url, params)
    json_dict = json.loads(res.text)

    company = Company()
    is_link = Financial_Statements_LinkOrBasic()
    year = Year()
    quarter = Quarter()
    fs_div = Financial_Statements_Div()
    fs_a = FS_Account()

    items = ["rcept_no","reprt_code","bsns_year","sj_div","sj_nm","account_nm","account_detail","thstrm_amount"]
    item_names = ["접수번호","보고서코드","사업연도","재무제표구분","재무제표명","계정명","계정상세","당기금액"]
    data_fi= []
    if json_dict['status'] == "000": # 정상적으로 데이터 가져옴
        company.company_name = company_name_
        year.bsns_year = year_
        if quarter_ == "11013":
                quarter.quarter_name = "1/4"
        elif quarter_ == "11012":
            quarter.quarter_name = "2/4"
        elif quarter_ == "11014":
            quarter.quarter_name = "3/4"
        elif quarter_ == "11011":
            quarter.quarter_name = "4/4"
            
        if link == "CFS":
            is_link.linkOrbasic = "linked"
        else:
            is_link.linkOrbasic = "basic"

        for fs_lst in json_dict['list']: # 한 행씩 가져오기
            
            if fs_lst["sj_div"] == "BS":
                fs_div.sj_div = "BS"
            elif fs_lst["sj_div"] == "IS":
                fs_div.sj_div = "IS"
            elif fs_lst["sj_div"] == "CIS":
                fs_div.sj_div = "CIS"
            elif fs_lst["sj_div"] == "CF":
                fs_div.sj_div = "CF"
            elif fs_lst["sj_div"] == "SCE":
                fs_div.sj_div = "SCE"

            fs_a.account_name = fs_lst["account_nm"]
            fs_a.a = fs_lst["thstrm_amount"]
            
            fs_a.financial_statements_div = fs_div
            fs_a.save()
            fs_div.lb = is_link
            fs_div.save()
            is_link.quarter = quarter
            is_link.save()
            quarter.year = year
            quarter.save()
            year.company = company
            year.save()

# financial_data(api_key,"00126380")


if __name__ == "__main__":
    # first
    # DART_data = dart_unique_key(api_key)
    # for data in DART_data:
    #     unique_code(dart_code=data[0],company_name_u=data[1],short_code=data[2],lastest_change=data[3]).save()
    #second
    linklst = ["CFS", "OFS"] # link, basic
    dart_codes = unique_code.objects.all()
    for code in dart_codes:
        if code.dart_code == "00274933":
            print(code.dart_code, code.company_name_u)
            make_financial_state(api_key, code.company_name_u, code.dart_code, "2019", "11011", "CFS")




