from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Company
from django.http import HttpResponse
# Create your views here.

from .crawling.crawling import *
from .crawling.crawling_library import API_KEY

api_key = API_KEY.APIKEY

class View_All_Data(ListView):
  model = Company
  context_object_name = "company_data"
  template_name='DBmanageapp/manager.html'
  paginat_by = 30

def Crawling_Data(request):
  Save_Dart_Data(api_key)
  return redirect('DBmanageapp:company_list')
  