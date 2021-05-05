from django.contrib import admin

# Register your models here.
from .models import Company, Quarter, Financial_Statements

# class CompanyAdmin(admin.ModelAdmin):
#     search_fields = ['company_name']
#     list_display = ('company_name', 'fs')
    
# admin.site.register(Company, CompanyAdmin)
# admin.site.register(Quarter)
# admin.site.register(Financial_Statements)
