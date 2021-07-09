from django.contrib import admin

# Register your models here.
from .models import Company, Year, Quarter, FS_Div, \
    FS_LoB, FS_Account, Dart

# class CompanyAdmin(admin.ModelAdmin):
#     search_fields = ['company_name']
#     list_display = ('company_name', 'fs')
    
admin.site.register(Company)
admin.site.register(Year)
admin.site.register(Quarter)
admin.site.register(FS_LoB)
admin.site.register(FS_Div)
admin.site.register(FS_Account)
admin.site.register(Dart)