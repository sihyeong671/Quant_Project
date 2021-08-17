import json
import os
import django
import time
from datetime import date
from pykrx import stock

from DBmanageapp.models import *
from .dart_crawling import *
from .API_KEY import *

#
def Save_FS_Data(api_key):
    linklst = ["CFS", "OFS"] # link, basic
    # years = ["2015","2016","2017","2018","2019","2020"]
    years = ["2018","2019","2020"]

    quarters = ["11013", "11014", "11012", "11011"]

    dart_codes = Dart.objects.all()
    company_list = Company.objects.all()
    count = 0

    for dart_data in dart_codes:
        company, flag = Company.objects.get_or_create(
            company_name=dart_data.company_name_dart, \
                short_code=dart_data.short_code
        )
        print(company.company_name)
        for y in years:
            year, flag = Year.objects.get_or_create(bs_year=int(y), company=company)
            for q in quarters:
                quarter, flag = Quarter.objects.get_or_create(qt_name=q, year=year)
                for l in linklst:
                    link, check = FS_LoB.objects.get_or_create(lob=l, quarter=quarter)
                    if check and not link.exist:
                        count += 1
                        time.sleep(0.1)
                        if count == 100:
                            return
                        Get_Amount_Data(api_key, dart_data.dart_code, y, q, l, link)
                        # 정정공시 따로 함수 만들기
                        
    
# update
                
    

    

