from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.db.models import Q, F

from api.mixins import ApiAuthMixin, PublicApiMixin
from stockmanage.models import Company, FS_Account, SUB_Account, Daily_Price
from stockmanage.utils import getData



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


class AccountApi(PublicApiMixin, APIView):
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
                'sub_account': sub_account_list,
            }
            fs_account_list.append(fsaccount)
        
        data = {
            'account': fs_account_list
        }
        
        return Response(data, status=status.HTTP_200_OK)


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
        
    