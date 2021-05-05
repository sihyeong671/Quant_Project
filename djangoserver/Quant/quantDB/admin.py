from django.contrib import admin

# Register your models here.
from .models import Company, Year, Quarter, Financial_Statements_Div, \
    Financial_Statements_LinkOrBasic, FS_Account

# class CompanyAdmin(admin.ModelAdmin):
#     search_fields = ['company_name']
#     list_display = ('company_name', 'fs')
    
admin.site.register(Company)
admin.site.register(Year)
admin.site.register(Quarter)
admin.site.register(Financial_Statements_LinkOrBasic)
admin.site.register(Financial_Statements_Div)
admin.site.register(FS_Account)
