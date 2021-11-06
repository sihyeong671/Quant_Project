from os import stat
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.db.models import Q, F
from django.http.response import HttpResponse


from api.mixins import ApiAuthMixin, PublicApiMixin, SuperUserMixin
from stockmanage.models import Company, FS_Account, SUB_Account, Daily_Price,\
    CustomFS_Account, CustomSUB_Account, UserCustomBS
from stockmanage.utils import getData

from crawling.crawling import *
from crawling.API_KEY import *
from stockmanage.models import *


class CompanyNameApi(PublicApiMixin, APIView):
    def get(self, request, *args, **kwargs):
        company_list = Company.objects.all()
        data_list = []
        
        for com in company_list:
            company = {
                'name': com.corp_name,
                'code': com.stock_code,
            }
            data_list.append(company)
        
        
        data = {
            'company': data_list
        }
        
        return Response(data, status=status.HTTP_200_OK)                      


class AccountSearchApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        stock_code = request.data.get('id', '')
        year = request.data.get('year', '')
        year = int(year)
        quarter = request.data.get('quarter', '')
        link = request.data.get('link', '')
        fs = request.data.get('fs')
        
        account_list = FS_Account.objects.\
            prefetch_related('sub_account')\
            .filter(
                Q(fs_div__sj_div=fs) &
                Q(fs_div__lob__lob=link) & 
                Q(fs_div__lob__quarter__qt_name=quarter) & 
                Q(fs_div__lob__quarter__year__bs_year=year) & 
                Q(fs_div__lob__quarter__year__company__stock_code=stock_code)
            )
        
        fs_account_list = []
        
        for ac in account_list:
            sub_account_list = []
            for sub in ac.sub_account.all():
                subaccount = {
                    'name': sub.account_name,
                    'amount': sub.account_amount,
                    'coef': 1,
                }
                sub_account_list.append(subaccount)
            
            fsaccount = {
                'fsname': ac.account_name,
                'amount': ac.account_amount,
                'coef': 1,
                'sub_account': sub_account_list,
            }
            fs_account_list.append(fsaccount)
        
        data = {
            'account': fs_account_list
        }
        
        return Response(data, status=status.HTTP_200_OK)


class CustomBSApi(ApiAuthMixin, APIView):
    def get(self, request, *args, **kwargs):
        custom_title = request.GET["title"]
        user = request.user
        bs_queryset = UserCustomBS.objects\
            .prefetch_related('custom_bs')\
            .filter(
                Q(user=user)
            )\
            .prefetch_related('custom_bs__')
        
        queryset = UserCustomBS.objects.get(user==)
        
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        stock_code = request.data.get('code', '')
        year = request.data.get('year', '')
        custom_title = request.data.get('title', '')
        quarter = request.data.get('quarter', '')
        fs = request.data.get('fs', '')
        link = request.data.get('link', '')
        account_list = request.data.getlist('account')
        
        profile = request.user.profile
        
        try:
            userbs = UserCustomBS(
                custom_title=custom_title,
                stock_code=stock_code,
                bs_year=year,
                qt_name=quarter,
                lob=link,
                sj_div=fs
            )
            userbs.save()
            profile.custom_bs = userbs
            
            for account in account_list:
                fsname = account['fsname']
                amount = account['amount']
                coef = account['coef']
                if coef == '':
                    coef = 1
                
                custom_fsaccount = CustomFS_Account(
                    custom_bs=userbs,
                    account_name=fsname,
                    account_amount=amount,
                    coef=coef
                )
                custom_fsaccount.save()
                
                for sub in account['sub_account']:
                    subname = sub['name']
                    subamount = sub['amount']
                    subcoef = sub['coef']
                    if subcoef == '':
                        subcoef = 1
                    
                    custom_subaccount = CustomSUB_Account(
                        account_name=subname,
                        account_amount=subamount,
                        coef=subcoef
                    )
                    custom_subaccount.save()
            
            return Response({
                'message': 'Recieved succesfully',
                }, status=status.HTTP_200_OK)
        except:
            return Response({
                'message': "Recieve failed",
            }, status=status.HTTP_402_PAYMENT_REQUIRED)


class DailyPriceApi(PublicApiMixin, APIView):
    def post(self, request, *args, **kwargs):
        company_code = request.data.getlist('code')
        data = {}
        
        for code in company_code:
            company = Company.objects.filter(stock_code=code)
            
            if not company.exists():
                return Response({
                    "message": "Company not exists"
                }, status=status.HTTP_404_NOT_FOUND)
            
            company = company.first()
            
            stocks = Daily_Price.objects.filter(company__id=company.id).order_by('date')
            
            data[company.corp_name] = getData(stocks)
        
        return Response(data, status=status.HTTP_200_OK)
        

class Crawling_Data(SuperUserMixin, APIView):
    def get(self, request):
        apikey = APIKEY
        
        Save_FS_Data(apikey)
        Save_Price()
        
        queryset = Company.objects.all()
        
        companies = []
        
        for com in queryset:
            companies.append(com.corp_name)
            
        data = {
            'company': companies,
        }

        return Response(data, status=status.HTTP_200_OK)