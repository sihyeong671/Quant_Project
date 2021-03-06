from time import strptime, mktime
import pandas as pd

from django.db.models import Q, F


from stockmanage.models import FS_LoB

def getData(stocks):
    close_list = []

    for stock in stocks:
        times = strptime(str(stock.date), '%Y-%m-%d')
        utc_now = mktime(times) * 1000

        close_list.append([utc_now, stock.close, stock.per, stock.pbr])

    return close_list


def getCaseData(case, condition, queryset):
    allcnt = FS_LoB.objects.filter(
        condition
    ).count()
    comp_num = int(allcnt * case[2] / 100.0)
    
    ## =====================
    ## |  Case Field : ROE |
    ## =====================
    if case[0] == "ROE":
        condition.add(~Q(ROE=0), Q.AND)
        condition.add(~Q(ROE=None), Q.AND)
        if case[1] == 1:
            # 상위
            queryset = queryset.filter(
                condition
            ).order_by('-ROE').values()[:comp_num]
            
        elif case[1] == 0:
            #하위
            queryset = queryset.filter(
                condition
            ).order_by('ROE').values()[:comp_num]
            
        elif case[1] == 3:
            #이상
            condition.add(Q(ROE__gte=case[2]), Q.AND)
            queryset = queryset.filter(
                condition
            ).values()
            
        elif case[1] == 2:
            #이하
            condition.add(Q(ROE__lte=case[2]), Q.AND)
            queryset = queryset.filter(
                condition
            ).values()
    
    
    ## =====================
    ## |  Case Field : ROA |
    ## =====================
    if case[0] == "ROA":
        condition.add(~Q(ROA=0), Q.AND)
        condition.add(~Q(ROA=None), Q.AND)
        if case[1] == 1:
            # 상위
            queryset = queryset.filter(
                condition
            ).order_by('-ROA')[:comp_num].values()
            
        elif case[1] == 0:
            #하위
            queryset = queryset.filter(
                condition
            ).order_by('ROA')[:comp_num].values()
            
        elif case[1] == 3:
            #이상
            condition.add(Q(ROA__gte=case[2]), Q.AND)
            queryset = queryset.filter(
                condition
            ).values()
            
        elif case[1] == 2:
            #이하
            condition.add(Q(ROA__lte=case[2]), Q.AND)
            queryset = queryset.filter(
                condition
            ).values()
    
    
    ## =====================
    ## |  Case Field : GPA |
    ## =====================
    if case[0] == "GPA":
        condition.add(~Q(GPA=0), Q.AND)
        condition.add(~Q(GPA=None), Q.AND)
        if case[1] == 1:
            # 상위
            queryset = queryset.filter(
                condition
            ).order_by('-GPA')[:comp_num].values()
            
        elif case[1] == 0:
            #하위
            queryset = queryset.filter(
                condition
            ).order_by('GPA')[:comp_num].values()
            
        elif case[1] == 3:
            #이상
            condition.add(Q(GPA__gte=case[2]), Q.AND)
            queryset = queryset.filter(
                condition
            ).values()
            
        elif case[1] == 2:
            #이하
            condition.add(Q(GPA__lte=case[2]), Q.AND)
            queryset = queryset.filter(
                condition
            ).values()
    
    return pd.DataFrame(list(queryset))
    