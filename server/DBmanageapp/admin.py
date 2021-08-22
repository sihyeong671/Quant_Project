from django.contrib import admin
from .models import Dart, Company, Year, Quarter, FS_LoB, FS_Div, FS_Account, SUB_Account, Daily_Price


admin.site.register(Dart)
admin.site.register(Company)
admin.site.register(Year)
admin.site.register(Quarter)
admin.site.register(FS_LoB)
admin.site.register(FS_Div)
admin.site.register(FS_Account)
admin.site.register(SUB_Account)
admin.site.register(Daily_Price)

