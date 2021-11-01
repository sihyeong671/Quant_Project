import os

from rest_framework.views import APIView

from django.http import FileResponse
from django.http.response import Http404
from django.conf import settings

from api.mixins import PublicApiMixin

BASE_DIR = settings.BASE_DIR

class GetLogApi(PublicApiMixin, APIView):
    def get(self, request):
        file_path = os.path.join(BASE_DIR, 'logs/quantlog.log')

        try:
            return FileResponse(open(file_path, 'rb'))
        except:
            raise Http404()