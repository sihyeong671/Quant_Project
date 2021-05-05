from django.contrib import admin

from .models import Company, Financial_Statements_LinkOrBasic,\
     Financial_Statements_Div, Quarter, Year, FS_Account

# class CompanyAdmin(admin.ModelAdmin):
#     search_fields = ['company_name']
#     list_display = ('company_name', 'fs')
    
admin.site.register(Company)
admin.site.register(Financial_Statements_LinkOrBasic)
admin.site.register(Financial_Statements_Div)
admin.site.register(Quarter)
admin.site.register(Year)
admin.site.register(FS_Account)
