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





