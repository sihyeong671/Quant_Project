import requests as rq
import pandas as pd
from io import BytesIO
import zipfile
import xml.etree.ElementTree as et
import json
import API_KEY

pd.set_option('display.max_row', 300) # 행 갯수 늘려서 보는 옵션
# pd.set_option('display.max_column', 100) # 열 갯수 늘려서 보는 옵션 

# krx에서 정보 가져오기
def krx_corporation():
    generate_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    generate_param = {
        "mktId": "ALL",
        "share": 1,
        "csvxls_isNo": "false", # 엑셀 다운로드
        "name": "fileDown",
        "url": "dbms/MDC/STAT/standard/MDCSTAT01901"
        }
    # 본인의 user-agent 삽입
    headers = {
        'User-Agent' : API_KEY.USERAGENT
        }

    resp = rq.post(generate_url,generate_param)
    code = resp.content

    download_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
    download_param = {'code' : code}

    _resp = rq.post(download_url, download_param, headers=headers)
    df = pd.read_excel(BytesIO(_resp.content))
    print(df)


def dart_unique_key(api_key):
    # dart에서 고유번호 가져오기
    items = ["corp_code", "corp_name", "stock_code", "modify_date"]  # OpenApi에서 주는 정보
    item_names = ["고유번호", "회사명", "종목코드", "최종변경일자"]
    url = "https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={}".format(api_key)
    resp = rq.get(url)
    zfile = zipfile.ZipFile(BytesIO(resp.content))
    fin = zfile.open(zfile.namelist()[0])  # 압축파일 내의 CORPCODE.xml 열기
    # xml 파일 파싱하기
    root = et.fromstring(fin.read().decode('utf-8'))
    # print(root)
    data_code = []
    for child in root:
        # 상장회사만 가져오기
        if len(child.find('stock_code').text.strip()) > 1:  # stock_code 없는 기업 제외
            data_code.append([])
            for item in items:
                data_code[-1].append(child.find(item).text)
    df_dart = pd.DataFrame(data_code, columns=item_names)
    print(df_dart)

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
        for line in json_dict['list']: 
            data_fi.append([])
            for itm in items:
                if itm in line.keys(): # itm append
                    data_fi[-1].append(line[itm])
                else:
                    data_fi[-1].append('') # 내용없을시 공백
    df_fi = pd.DataFrame(data_fi, columns =item_names)
    print(df_fi)
api_key = API_KEY.APIKEY
# financial_data(api_key,"00126380")
dart_unique_key(api_key)
# 모든 고유번호 가져오기
# 모든 고유번호 for 문으로 돌리면서 재무제표 가져오기
