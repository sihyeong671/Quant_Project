import requests as rq
import json
import xml.etree.ElementTree as et
import zipfile
from datetime import datetime
from io import BytesIO
from bs4 import BeautifulSoup
import re

from django.db import transaction

from crawling.krx_crawling import Get_Krx_Short_Code

from stockmanage.models import FS_Div, FS_Account, FS_LoB, SUB_Account, Dart, Company


#  개별로 실행하면 생기기는 문제 해결을 위한 코드
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# print(datetime.today().strftime("%Y%m%d"))

def find_parameter(string: str, fs_name: str) -> list:
    p = re.compile('"[a-zA-Z0-9]*"')
    idx_start = string.find(fs_name)
    idx_end = string.find('cnt++', idx_start)
    string_limit = string[idx_start:idx_end]
    parameters = p.findall(string_limit)
    lst = []
    for param in parameters:
        lst.append(param.replace('"', ""))
    return lst


def Print_Error(status: str):
    if  status == "010":
        print('등록되지 않은 키입니다.')
    elif status == "011":
        print('사용할 수 없는 키입니다')            
    elif status == "013":
        print('no data')
    elif status == "020":
        print('요청 제한을 초과하였습니다.')        
    elif status == "100":
        print('unvaild value')
    elif status == "800":
        print('원활한 공시서비스를 위하여 오픈API 서비스가 중지 중입니다.')
    elif status == "900":
        print('정의되지 않은 오류가 발생하였습니다.')


# dart에서 고유번호 가져오기
def Dart_Unique_Key(api_key):
    """
    Krx에서 상장한 회사들만 Dart에서 고유번호 가져오기 
    """

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

@transaction.atomic
def Get_Amount_Data(api_key,corp_code,year,quarter,link_state, link_model):
    """
    기업코드, 년도, 분기, 연결/일반, link모델 매개변수
    매개변수에 맞는 재무제표 정보가져오고 dart홈페이지에서 BS 하위관계를 알기위해 실제 재무제표 스크래핑
    재무제표 데이터 for문으로 fs_account모델에 저장
    """
    dart_url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?"
    params = {
        'crtfc_key': api_key, 'corp_code': corp_code, 
        'bsns_year': year, 'reprt_code': quarter, 'fs_div': link_state}
    res = rq.get(dart_url, params)
    json_dict = json.loads(res.text)

    if json_dict['status'] == "000": # 정상적으로 데이터 가져옴

        #ROE, ROA
        net_income = 0
        total_capital = 0
        total_asset = 0

        link_model.exist = 1

        report_number = json_dict['list'][0]['rcept_no']

        fs_url = f'http://dart.fss.or.kr/dsaf001/main.do?rcpNo={report_number}'
        fs_res = rq.get(fs_url)

        fs_soup = BeautifulSoup(fs_res.text, "lxml")
        script_content = str(fs_soup.find_all('script')[-2].string)

        if link_state == "CFS":
            parameter_list = find_parameter(script_content, "연결재무제표")
        else:
            parameter_list = find_parameter(script_content, " 재무제표")

        bs_url = f"http://dart.fss.or.kr/report/viewer.do?rcpNo={parameter_list[1]}" \
        f"&dcmNo={parameter_list[2]}" \
        f"&eleId={parameter_list[3]}" \
        f"&offset={parameter_list[4]}" \
        f"&length={parameter_list[5]}" \
        f"&dtd={parameter_list[6]}"

        bs_res = rq.get(bs_url)
        bs_soup = BeautifulSoup(bs_res.text, "lxml") # html.parser 도 가능
        
        print("=======")
        print(link_model.quarter.year.company.corp_name)
        print(link_model.quarter.year.bs_year)
        print(link_model.quarter.qt_name)
        print(link_state)
        print("=======")
        
        # try:
        fs_unit = bs_soup.find("table").find_all('p')[-1]
        link_model.unit = fs_unit.text
        link_model.save()
        # except Exception as ex:
        #     print("Error Raised: ", ex)
        
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
        
        # print("bs_tree : ", bs_tree)
        
        BS = FS_Div(sj_div="BS", lob=link_model)
        BS.save()
        
        IS = FS_Div(sj_div="IS",lob=link_model)
        IS.save()
        
        CIS = FS_Div(sj_div="CIS",lob=link_model)
        CIS.save()

        CF = FS_Div(sj_div="CF",lob=link_model)
        CF.save()
        
        SCE = FS_Div(sj_div="SCE",lob=link_model)
        SCE.save()
        
        gp = 0.0
        all_amount = 1.0
        
        pre_money = {}
        for fs_lst in json_dict['list']: # 한 행씩 가져오기
            money = FS_Account()
            if fs_lst["sj_div"] == "BS":
                if fs_lst["account_nm"] in bs_tree.keys():
                    money.fs_div = BS
                    pre_money = money

                    if fs_lst["account_nm"] == "자산총계":
                        total_asset = int(fs_lst["thstrm_amount"])
                    elif fs_lst["account_nm"] == "자본총계":
                        total_capital = int(fs_lst["thstrm_amount"])
                        link_model.total_capital = total_capital
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

            elif fs_lst["sj_div"] == "CIS": # 포괄 손익 계산서
                money.fs_div = CIS
                if "당기순이익" in "".join(fs_lst["account_nm"].split()):
                    print("".join(fs_lst["account_nm"].split()))
                    print(fs_lst["thstrm_amount"])
                    try:
                        net_income = float(fs_lst["thstrm_amount"])
                        link_model.net_income += net_income
                    except:
                        pass
                    
                if fs_lst["thstrm_add_amount"] == '': # 누적 금액
                    money.account_add_amount = 0
                else:
                    money.account_add_amount = fs_lst["thstrm_add_amount"]

            elif fs_lst["sj_div"] == "CF":
                money.fs_div = CF

            elif fs_lst["sj_div"] == "SCE":
                money.fs_div = SCE
            
            account_name = fs_lst["account_nm"].split()
            account_name = "".join(account_name)
                    
            money.account_name = account_name
            money.account_detail = fs_lst["account_detail"]
            

            if fs_lst["thstrm_amount"] == '': # 당기 금액
                money.account_amount = 0
            else:
                money.account_amount = fs_lst["thstrm_amount"]
                if "매출총이익" in account_name or "매출총손익" in account_name:
                    gp = float(fs_lst["thstrm_amount"])
                elif "자산총계" in account_name:
                    all_amount = float(fs_lst["thstrm_amount"])
            
            money.save()
        
        try:
            link_model.GPA = gp/all_amount
            link_model.ROA = net_income / total_asset * 100 # %
            link_model.ROE = net_income / total_capital * 100 # %
            
            link_model.save()
            
        except:
            print("Link model save failed..")
    

    else:
        if json_dict['status'] == "013":
            link_model.save()
        Print_Error(json_dict['status'])



def Save_Dart_Data(api_key):
    """
    가장 먼저 실행
    상장된 기업의 Dart 고유번호 가져와서 Dart모델에 저장하는 함수
    """
    dart_data = Dart_Unique_Key(api_key)
    for data in dart_data:
        Dart(dart_code=data[0],company_name_dart=data[1],
             short_code=data[2],recent_modify=data[3]).save()


def Save_Corp_Info(api_key, code, company):
    """
    code의 기업 개황(정보)가져와서 Company모델에 저장하는 함수
    """
    url = 'https://opendart.fss.or.kr/api/company.json'
    param = {
        'crtfc_key': api_key,
        'corp_code':code
    }
    try:
        res = rq.get(url, param)
        # json을 딕셔너리 객체로 디코딩
        json_dict = json.loads(res.text)
        if json_dict['status'] == '000':
            company.corp_name = json_dict['corp_name']
            company.corp_namge_eng = json_dict['corp_name_eng']
            company.stock_name = json_dict['stock_name']
            company.ceo_name = json_dict['ceo_nm']
            company.corp_cls = json_dict['corp_cls']
            company.jurir_no = json_dict['jurir_no']
            company.bizr_no = json_dict['bizr_no']
            company.adres = json_dict['adres']
            company.hm_url = json_dict['hm_url']
            company.ir_url = json_dict['ir_url']
            company.phn_no = json_dict['phn_no']
            company.fax_no = json_dict['fax_no']
            company.induty_code = json_dict['induty_code']
            company.est_dt = json_dict['est_dt']
            company.acc_mt = json_dict['acc_mt']
            
            company.save()
            print(company.corp_name, " saved")
    except:
        print('error')