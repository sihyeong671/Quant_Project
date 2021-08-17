from django.shortcuts import render, redirect
from django.views.generic import ListView
# from django.views.generic.list import MultipleObjectMixin

from .models import Company, FS_Account
from django.http import HttpResponse
# Create your views here.

from .crawling import *
from .API_KEY import *
from .models import *


class View_All_Data(ListView):
  model = Company
  context_object_name = "company_data"
  template_name='DBmanageapp/manager.html'
  paginat_by = 30
  
  # def get_context_data(self, **kwargs):
  #     context = super().get_context_data(**kwargs)
  #     context["company_temp"] = Company.objects.get(company_name="엑세스바이오")
  #     return context
  
def Crawling_Data(request):
  Save_Dart_Data(APIKEY)
  
  return redirect('DBmanageapp:company_list')
  

