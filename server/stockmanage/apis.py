from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from api.mixins import ApiAuthMixin, PublicApiMixin
from stockmanage.models import Company


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
    