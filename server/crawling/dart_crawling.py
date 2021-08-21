import requests as rq
import json
import xml.etree.ElementTree as et
import zipfile
from datetime import datetime
from io import BytesIO
from bs4 import BeautifulSoup

from crawling.krx_crawling import Get_Krx_Short_Code

from DBmanageapp.models import FS_Div, FS_Account, SUB_Account, Dart


#  개별로 실행하면 생기기는 문제 해결을 위한 코드
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# print(datetime.today().strftime("%Y%m%d"))

# 재무제표 viewDoc파라미터 찾기
def find_parameter(string: str, fs_name: str) -> list:
    pointer_1 = 0
    pointer_2 = 0

    for i in range(2000, len(string)):
        if string[i-len(fs_name):i] == fs_name:
            for j in range(i, len(string)):
                if string[j-7:j] == "viewDoc":
                    pointer_1 = j
                    continue
                elif string[j] == ";":
                    pointer_2 = j
                    param = string[pointer_1+1:pointer_2-1]
                    lst = param.replace("'", "").split(", ")
                    return lst


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

    dart_url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
    params = {'crtfc_key': api_key, 'corp_code': corp_code, 'bsns_year': year, 'reprt_code': quarter, 'fs_div': link_state}
    res = rq.get(dart_url, params)
    json_dict = json.loads(res.text)

    if json_dict['status'] == "000": # 정상적으로 데이터 가져옴

        link_model.exist = 1
        link_model.save()

        report_number = json_dict['list'][0]['rcept_no']

        fs_url = f'http://dart.fss.or.kr/dsaf001/main.do?rcpNo={report_number}'
        fs_res = rq.get(fs_url)

        fs_soup = BeautifulSoup(fs_res.text, "lxml")
        script_content = str(fs_soup.find_all('script')[-2].string)

        if link_state == "CFS":
            parameter_list = find_parameter(script_content, "연결재무제표")
        else:
            parameter_list = find_parameter(script_content, "재무제표")

        bs_url = f"http://dart.fss.or.kr/report/viewer.do?rcpNo={parameter_list[0]}" \
        f"&dcmNo={parameter_list[1]}" \
        f"&eleId={parameter_list[2]}" \
        f"&offset={parameter_list[3]}" \
        f"&length={parameter_list[4]}" \
        f"&dtd={parameter_list[5]}"

        bs_res = rq.get(bs_url)
        bs_soup = BeautifulSoup(bs_res.text, "lxml") # html.parser 도 가능

        bs_tree = {}
        now = ''
        for a in bs_soup.find_all("p"):
            account = a.text
            if len(account) > 0:
                if account[0] == '　':
                    if account[1] == '　':
                        if account[2] == '　':
                            continue
                        bs_tree[now].append(account.replace('　', ""))
                    else:
                        now = account.replace('　', "")
                        bs_tree[now] = []
            if account == "자본과부채총계":
                break

        
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

        pre_money = {}
        for fs_lst in json_dict['list']: # 한 행씩 가져오기
            money = FS_Account()
            if fs_lst["sj_div"] == "BS":
                if fs_lst["account_nm"] in bs_tree.keys():
                    money.fs_div = BS
                    pre_money = money
                else:
                    for child in bs_tree.values():
                        if fs_lst["account_nm"] in child:
                            sub_money = SUB_Account()
                            sub_money.pre_account = pre_money
                            sub_money.account_name = fs_lst["account_nm"]
                            sub_money.account_detail = fs_lst["account_detail"]
                            if fs_lst["thstrm_amount"] == '':
                                sub_money.account_amount = 0
                            else:
                                sub_money.account_amount = fs_lst["thstrm_amount"]
                            sub_money.save()
                            break
                    continue
            elif fs_lst["sj_div"] == "IS":
                money.fs_div = IS

            elif fs_lst["sj_div"] == "CIS":
                money.fs_div = CIS

            elif fs_lst["sj_div"] == "CF":
                money.fs_div = CF

            elif fs_lst["sj_div"] == "SCE":
                money.fs_div = SCE
            
            money.account_name = fs_lst["account_nm"]
            money.account_detail = fs_lst["account_detail"]

            if fs_lst["thstrm_amount"] == '':
                money.account_amount = 0
            else:
                money.account_amount = fs_lst["thstrm_amount"]

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
            
            
def Save_Dart_Data(api_key):
    dart_data = Dart_Unique_Key(api_key)
    for data in dart_data:
        Dart(dart_code=data[0],company_name_dart=data[1],
             short_code=data[2],recent_modify=data[3]).save()
