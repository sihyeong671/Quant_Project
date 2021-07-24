from django.shortcuts import render
from django.views.generic import ListView

from .models import Company
# Create your views here.

class View_All_Data(ListView):
    model = Company
    context_object_name = "company_data"
    template_name='DBmanageapp/manager.html'
    paginat_by = 30


