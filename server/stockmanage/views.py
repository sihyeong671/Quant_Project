from django.shortcuts import render, redirect
from django.views.generic import ListView
# from django.views.generic.list import MultipleObjectMixin

from .models import Company, FS_Account
from django.http import HttpResponse

from crawling.crawling import *
from crawling.API_KEY import *
from stockmanage.models import *



def Crawling_Data(request):

    apikey = APIKEY
    # Save_Dart_Data(apikey)
    Save_FS_Data(apikey)
    Save_Price()

    # company_list = Company.objects.all()

    # for com in company_list:
    #     com.delete()

    return HttpResponse("good")
  

