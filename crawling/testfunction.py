import requests as rq
import pandas as pd
from io import BytesIO

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