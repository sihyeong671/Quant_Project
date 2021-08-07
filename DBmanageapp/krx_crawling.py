import requests as rq
import pandas as pd
from io import BytesIO
from pykrx import stock

## UERAGENT##
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
    
    # return corp['종목코드']
    return corp


# 상장기업 단축코드 가져오기
def Get_Krx_Short_Code(day:str) -> list:

	# list
	short_code = stock.get_market_ticker_list(day, market="ALL")
	return short_code



def Get_Krx_Ohlv(day:str):
	pass


# PBR, PER
def Daily_Crawling(day:str):
    df_market_cap = stock.get_market_cap_by_ticker(day, market="ALL") # index -> ticker == shortcode
    df_p2 = stock.get_market_fundamental_by_ticker(day, market="ALL")

    # print(df_market_cap)
    # print(df_p2)





