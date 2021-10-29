from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

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
    def get(self, request, *args, **kwargs):
        
        account_list = FS_Account.objects.all()
        
        fs_account_list = []
        
        for ac in account_list:
            sub_account_list = []
            for sub in ac.sub_account.all():
                subaccount = {
                    'name': sub.account_name,
                    'amount': sub.account_amount
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
    def get(self, request, *args, **kwargs):
        com = get_object_or_404(Company, stock_code=kwargs['code'])
        stocks = Daily_Price.objects.filter(company__id=com.id).order_by('date')
        data = getData(stocks)
        return Response(data)
    