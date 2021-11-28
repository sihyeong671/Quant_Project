from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from api.mixins import SuperUserMixin, CrawlerMixin
from stockmanage.models import Company
from stockmanage.models import *

from crawling.crawling import Save_Price, Save_Dart_Data, Save_FS_Data
from crawling.API_KEY import APIKEY



class Crawling_DailyPrice(CrawlerMixin, APIView):
    def get(self, request, *args, **kwargs):
        """
        주가 저장 API
        자세한 사항은 Save_Price() 함수 참고
        """
        Save_Price()
        
        return Response({
            "message": "successed save daily price"
        }, status=status.HTTP_200_OK)
        
        

class Crawling_Dart(CrawlerMixin, APIView):
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
        },status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        Dart.objects.all().delete()
        
        return Response({
            "message": "success delete dart data"
        },status=status.HTTP_204_NO_CONTENT)
    

class Crawling_FSData(CrawlerMixin, APIView):
    def get(self, request):
        apikey = APIKEY
        Save_FS_Data(apikey)
        
        return Response({
            'message': "Success crawled FS data",
        }, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        Company.objects.all().delete()
        
        return Response({
            "message": "success delete company"
        },status=status.HTTP_204_NO_CONTENT)
    
    