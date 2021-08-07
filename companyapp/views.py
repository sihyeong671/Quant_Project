from django.shortcuts import render
from django.views.generic.detail import DetailView
from DBmanageapp.models import Company

class CompanyDetailView(DetailView):
    model = Company
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        
        # 분기 입력 받기
        
        # 기업명 입력 받기 - 최대 4개
        
        context[""] = ""
        return context
    
