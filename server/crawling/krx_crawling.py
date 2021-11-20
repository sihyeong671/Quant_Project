import time
import requests as rq
import pandas as pd
from io import BytesIO
from pykrx import stock

## UERAGENT ##
from .API_KEY import USERAGENT


# 상장기업 정보 가져오기
def Get_Krx_Corp():
    
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
    headers = {'User-Agent': USERAGENT}
    generate_res = rq.post(generate_url, generate_param, headers = headers)
    code = generate_res.content

    download_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
    download_param = {'code': code}
    download_res = rq.post(download_url, download_param, headers = headers)

    corp = pd.read_excel(BytesIO(download_res.content), dtype={'종목코드': str})
    return corp['종목코드']
    # return corp


# 상장기업 단축코드 가져오기
def Get_Krx_Short_Code(day:str):

	# list
    short_code = stock.get_market_ticker_list(day, market="ALL")
    # print(short_code)
    return short_code



# 시가총액, ohlcv
def Daily_Crawling(start_date:str, end_date:str, code:str):
    # 위 순서대로
    df_market_cap = stock.get_market_cap_by_date(start_date, end_date, code)
    df_ohlcv = stock.get_market_ohlcv_by_date(start_date, end_date, code)
    df_fundamental = stock.get_market_fundamental_by_date(start_date, end_date, code)
    df = pd.concat([df_market_cap.iloc[:, 0], df_ohlcv, df_fundamental], axis=1)
    time.sleep(1)
    return df
