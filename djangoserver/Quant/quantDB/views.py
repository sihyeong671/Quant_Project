from django.shortcuts import render
from .models import Company, Financial_Statements, Quarter
# Create your views here.


def find_state(request):
    company_list = Company.objects.all()
    
    # start_date = request.stdate
    # end_date = request.eddate
    
    com_name_list = []
    b_list = []
    
    for com in company_list:
        fs_date = com.fs.quarter.stock_date
        # if fs_date >= start_date and fs_date <= end_date:
        # q_set = com.fs.quarter_set.all()
        # for q in q_set:
        b_list.append(com.fs.quarter.benefit)
        com_name_list.append(com.company_name)
    
    data_list = [b_list, com_name_list]
    
    context = {'b_list' : b_list, 'com_name_list' : com_name_list}
    
    return render(request, 'main.html', context)
    
def make_financial_state(request):
    items = ["rcept_no","reprt_code","bsns_year","sj_div","sj_nm","account_nm","account_detail","thstrm_nm","thstrm_amount"]
    item_names = ["접수번호","보고서코드","사업연도","재무제표구분","재무제표명","계정명","계정상세","당기명","당기금액"]
    
    # 기업 이름도 같이 보내오게
    json_dic = crawlfunc()
    company = Company()
    fs = Financial_Statements()
    quarter = Quarter()
    
    if json_dic['status'] == "000":
        company.company_name = c_name
        company.save()
        
        for fs_list in json_dict['list']:


import json
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
