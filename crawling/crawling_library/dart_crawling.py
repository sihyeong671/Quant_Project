from datetime import datetime
import xml.etree.ElementTree as et
import requests as rq
import zipfile
from io import BytesIO
import time
from krx_crawling import Get_Krx_Short_Code

# print(datetime.today().strftime("%Y%m%d"))


# dart에서 고유번호 가져오기
def Dart_Unique_Key(api_key) -> list:

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
    krx_short_code = Get_Krx_Short_Code(datetime.today().strftime("%Y%m%d"))
    for child in root:      
        # 상장회사만 가져오기
        dart_short_code = child.find('stock_code').text.strip()
        if dart_short_code in krx_short_code:
            data.append([])
            for item in items:
                data[-1].append(child.find(item).text)
    return data


def Get_Amount_Data(api_key,corp_code,year,quarter,link_state, link_model):

    url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
    params = {'crtfc_key': api_key, 'corp_code': corp_code, 'bsns_year': year, 'reprt_code': quarter, 'fs_div': link_state}
    res = rq.get(url, params)
    json_dict = json.loads(res.text)

    if json_dict['status'] == "000": # 정상적으로 데이터 가져옴
        BS = FS_Div()
        BS.sj_div = "BS"
        BS.lob = link_model
        BS.save()

        IS = FS_Div()
        IS.sj_div = "IS"
        IS.lob = link_model
        IS.save()
        
        CIS = FS_Div()
        CIS.sj_div = "CIS"
        CIS.lob = link_model
        CIS.save()

        CF = FS_Div()
        CF.sj_div = "CF"
        CF.lob = link_model
        CF.save()

        SCE = FS_Div()
        SCE.sj_div = "SCE"
        SCE.lob = link_model
        SCE.save()


        for fs_lst in json_dict['list']: # 한 행씩 가져오기
            money = FS_Account()
            money.account_name = fs_lst["account_nm"]
            money.account_detail = fs_lst["account_detail"]
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
        if json_dict['status'] == "010":
            print('등록되지 않은 키입니다.')
            print(corp_code, year, quarter, link_state)

        elif json_dict['status'] == "011":
            print('사용할 수 없는 키입니다')
            print(corp_code, year, quarter, link_state)
            
        elif json_dict['status'] == "013":
            print('no data')
            print(corp_code, year, quarter, link_state)

        elif json_dict['status'] == "020":
            print('요청 제한을 초과하였습니다.')
            print(corp_code, year, quarter, link_state)
        
        elif json_dict['status'] == "100":
            print('unvaild value')
            print(corp_code, year, quarter, link_state)

        elif json_dict['status'] == "800":
            print('원활한 공시서비스를 위하여 오픈API 서비스가 중지 중입니다.')
            print(corp_code, year, quarter, link_state)

        elif json_dict['status'] == "900":
            print('정의되지 않은 오류가 발생하였습니다.')
            print(corp_code, year, quarter, link_state)






