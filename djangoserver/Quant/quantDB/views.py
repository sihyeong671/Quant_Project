from django.shortcuts import render
from .models import Company, Financial_Statements_LinkOrBasic,\
     Financial_Statements_Div, Quarter, Year, FS_Account
import json
# Create your views here.


def find_state(request):
    company_list = Company.objects.all()
    
    # start_date = request.stdate
    # end_date = request.eddate
    
    # com_name_list = []
    # year_list = []
    # quarter_list = []
    
    
    # for com in company_list:
    #     b_list.append(com.fs.quarter.benefit)
    #     com_name_list.append(com.company_name)
    
    # data_list = [b_list, com_name_list]
    
    context = {'company_list' : company_list}
    
    return render(request, 'main.html', context)
    
def make_financial_state(request):
    items = ["rcept_no","reprt_code","bsns_year","sj_div","sj_nm","account_nm","account_detail","thstrm_nm","thstrm_amount"]
    item_names = ["접수번호","보고서코드","사업연도","재무제표구분","재무제표명","계정명","계정상세","당기명","당기금액"]
    
    # 기업 이름도 같이 보내오게
    json_dic, is_linked, cname = crawlfunc()
    
    company = Company()
    is_link = Financial_Statements_LinkOrBasic()
    year = Year()
    quarter = Quarter()
    fs_div = Financial_Statements_Div()
    fs_a = FS_Account()
    
    if json_dic['status'] == "000":
        company.company_name = c_name
        company.save()
        
        for fs_list in json_dict['list']:
            year.bsns_year = fs_list["bsns_year"]   # int로 변환해주기
            if fs_list["reprt_code"] == "11013":
                quarter.quarter_name = "1/4"
            elif fs_list["reprt_code"] == "11012":
                quarter.quarter_name = "2/4"
            elif fs_list["reprt_code"] == "11014":
                quarter.quarter_name = "3/4"
            elif fs_list["reprt_code"] == "11011":
                quarter.quarter_name = "4/4"
            
            if(is_linked == "CFS"):
                is_link.linkOrbasic = "linked"
            else:
                is_link.linkOrbasic = "basic"
            
            if fs_list["sj_div"] == "BS":
                fs_div.sj_div = "BS"
            elif fs_list["sj_div"] == "IS":
                fs_div.sj_div = "IS"
            
            fs_a.account_name = fs_list["account_nm"]
            fs_a.a = fs_list["thstrm_amount"]
            
            
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
            
            
def show_chart(request):
    chart_dataset = { 
        '1': 10, 
        '2': 30,
        '3': 45,
        '4': 70,
        '5': 20,
    } 
    chartJson = json.dumps(chart_dataset)
    context = {
        'chartJson' : chartJson,
    }
    return render(request, 'chart.html', context)