from datetime import datetime
from API_KEY import APIKEY
import xml.etree.ElementTree as et
import requests as rq
import zipfile
from io import BytesIO
import time
from krx_crawling import Get_Krx_Short_Code


# print(datetime.today().strftime("%Y%m%d"))


# dart에서 고유번호 가져오기
def Dart_Unique_Key(api_key):

    items = ["corp_code", "corp_name", "stock_code", "modify_date"]  # OpenApi에서 주는 정보
    # item_names = ["고유번호", "회사명", "종목코드", "최종변경일자"]
    url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={api_key}"
    resp = rq.get(url)

    zfile = zipfile.ZipFile(BytesIO(resp.content))
    # 압축파일 내의 CORPCODE.xml 열기
    tree = zfile.open(zfile.namelist()[0])  
    # xml 파일 파싱하기
    root = et.fromstring(tree.read().decode('utf-8'))
    
    data = []
    krx_short_code = list(Get_Krx_Corp())
    for child in root:      
        # 상장회사만 가져오기
        dart_short_code = child.find('stock_code').text.strip()
        if dart_short_code in krx_short_code:
            data.append([])
            for item in items:
                data[-1].append(child.find(item).text)
    return data









