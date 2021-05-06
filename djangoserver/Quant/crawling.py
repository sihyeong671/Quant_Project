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
from quantDB.models import unique_code

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
    
# 재무제표 가져오기
def financial_data(api_key, corp_code):
    url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
    # 연도별 for
    # 분기별 for
    # OFS 연결 재무제표, CFS 일반 재무제표
    params = {'crtfc_key': api_key, 'corp_code': corp_code, 'bsns_year': "2019", 'reprt_code': "11011", 'fs_div': "CFS"}
    # 연결재무제표없는 기업은 일반 재무제표를 가져와야 한다.
    res = rq.get(url, params)
    json_dict = json.loads(res.text)
    # print(json_dict)
    return json_dict, "CFS"
    items = ["rcept_no","reprt_code","bsns_year","sj_div","sj_nm","account_nm","account_detail","thstrm_amount"]
    item_names = ["접수번호","보고서코드","사업연도","재무제표구분","재무제표명","계정명","계정상세","당기금액"]
    data_fi= []
    if json_dict['status'] == "000": # 정상적으로 데이터 가져옴
        for line in json_dict['list']: # 한 행씩 가져오기

            data_fi.append([])
            for itm in items:
                if itm in line.keys(): # itm append
                    data_fi[-1].append(line[itm])
                else:
                    data_fi[-1].append('') # 내용없을시 공백
    df_fi = pd.DataFrame(data_fi, columns =item_names)
    print(df_fi)

# financial_data(api_key,"00126380")

if __name__ == "__main__":
    DART_data = dart_unique_key(api_key)
    for data in DART_data:
        unique_code(dart_code=data[0],company_name_u=data[1],short_code=data[2],lastest_change=data[3]).save()



