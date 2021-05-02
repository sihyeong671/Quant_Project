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
        for q in q_set:
            b_list.append(q.benefit)
            com_name_list.append(com.company_name)
    
    data_list = [b_list, com_name_list]
    
    context = {'b_list' : b_list, 'com_name_list' : com_name_list}
    
    return render(request, 'main.html', context)