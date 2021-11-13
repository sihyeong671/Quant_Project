from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from api.mixins import SuperUserMixin
from stockmanage.models import Company
from stockmanage.models import *

from crawling.crawling import *
from crawling.API_KEY import *



class Crawling_DailyPrice(SuperUserMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        주가 저장 API
        자세한 사항은 Save_Price() 함수 참고
        """
        try:
            Save_Price()
        except:
            return Response({
                "message": "failed save daily price"
            }, status=status.HTTP_409_CONFLICT)
        return Response({
            "message": "successed save daily price"
        })
        

class Crawling_Dart(SuperUserMixin, APIView):
    def get(self, request):
        try:
            apikey = APIKEY
            Save_Dart_Data(apikey)
        except:
            return Response({
                "message": "failed save dart data"
            }, status=status.HTTP_409_CONFLICT)
        
        return Response({
            "message": "success save dart data"
        },status=status.HTTP_200_OK)
    
    def delete(self, request):
        try:
            Dart.objects.all().delete()
        except:
            return Response({
                "message": "failed delete dart data"
            }, status=status.HTTP_409_CONFLICT)
        
        return Response({
            "message": "success delete dart data"
        },status=status.HTTP_200_OK)
    

class Crawling_FSData(SuperUserMixin, APIView):
    def get(self, request):
        try:
            apikey = APIKEY
            Save_FS_Data(apikey)
            Save_Price()
            
            queryset = Company.objects.all().values('corp_name')
            
            companies = []
            
            for com in queryset:
                companies.append(com.corp_name)
                
            data = {
                'company': companies,
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({
                "message": "failed save fs data"
            },status=status.HTTP_409_CONFLICT)
    
    def delete(self, request):
        try:
            Company.objects.all().delete()
        except:
            return Response({
                "message": "failed delete company"
            }, status=status.HTTP_409_CONFLICT)
        
        return Response({
            "message": "success delete company"
        },status=status.HTTP_200_OK)
    
    