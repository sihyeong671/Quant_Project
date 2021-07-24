from django.shortcuts import render, redirect

from .models import Company, FS_LoB,\
    FS_Div, Quarter, Year, FS_Account
import json
from django.http import HttpResponse
from django.db.models import Q

from .bs import list


def find_state(request):
    company_list = Company.objects.all()

    il = list

    context = {'company_list' : company_list, 'il' : il}
    
    # return render(request, 'chart/chart.html', context)
    return render(request, 'chart/chart.html', context)

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
               
    





