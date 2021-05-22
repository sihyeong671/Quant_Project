from django.shortcuts import render, redirect
from .models import Company, FS_LoB,\
    FS_Div, Quarter, Year, FS_Account
import json
from django.http import HttpResponse
from django.db.models import Q
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
    
    return render(request, 'chart.html', context)

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
    
def search_companyname(request):
    cname = request.GET.get('company_name', '')  # 회사명

    company_list = Company.objects.order_by('-company_name')
    if cname:
        company = company_list.filter(
            Q(company_name__icontains=cname) # 회사명 검색
        ).distinct()
    else:
        company = ""
        
    context = {"company" : company, "cname" : cname}
    return render(request, 'search.html', context)
               
    





