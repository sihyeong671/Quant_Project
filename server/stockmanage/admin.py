from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from stockmanage.models import *

admin.site.register(CustomFS_Account)
admin.site.register(CustomSUB_Account)
admin.site.register(UserCustomBS)


@admin.register(Dart)
class DartAdmin(admin.ModelAdmin):
    ordering = ('company_name_dart', )
    list_display = (
        'dart_code', 'company_name_dart', 'short_code', 
        'recent_modify',
    )
    list_display_links = (
        'dart_code', 'company_name_dart', 'short_code', 
        'recent_modify',
    )
    search_fields = (
        'dart_code', 'company_name_dart', 'short_code', 
        'recent_modify',
    )
    inlines = ()


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    ordering = ('corp_name', )
    list_display = (
        'corp_name', 'corp_name_eng', 'stock_name', 
        'stock_code','ceo_name', 
    )
    list_display_links = (
        'corp_name', 'corp_name_eng', 'stock_name', 
        'stock_code', 'ceo_name', 
    )
    search_fields = (
        'corp_name', 'corp_name_eng', 
        'stock_name', 'stock_code', 'ceo_name', 
    )
    inlines = ()


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    ordering = ('company__corp_name', )
    list_display = (
        'get_company', 'bs_year',
    )
    list_display_links = (
        'get_company', 'bs_year',
    )
    search_fields = ('company__corp_name', 'bs_year',)
    list_filter = ('bs_year', )
    
    list_select_related = [
        'company',
    ]
    
    inlines = ()
    
    def get_company(self, obj):
        company = obj.company.corp_name
        
        if not company:
            return ''
        return company
    get_company.short_description = _('Company')
    

@admin.register(Quarter)
class QuarterAdmin(admin.ModelAdmin):
    ordering = ('year__company__corp_name', )
    list_display = (
        'get_company', 'get_year', 'get_quarter', 
    )
    list_display_links = (
        'get_company', 'get_year', 'get_quarter', 
    )
    search_fields = (
        'year__company__corp_name', 'year__bs_year', 'qt_name', 
    )
    list_filter = ('qt_name', )
    
    list_select_related = [
        'year',
        'year__company',
    ]
    
    inlines = ()
    
    def get_quarter(self, obj):
        if obj.qt_name == "11013":
            return "1??????"
        elif obj.qt_name == "11012":
            return "2??????"
        elif obj.qt_name == "11014":
            return "3?????? ?????????"
        elif obj.qt_name == "11011":
            return "?????? ?????????"
        else:
            return ''
    get_quarter.short_description = _('Quarter')
    
    def get_company(self, obj):
        company = obj.year.company.corp_name
        
        if not company:
            return ''
        return company
    get_company.short_description = _('Company')
    
    def get_year(self, obj):
        year = obj.year.bs_year
        
        if not year:
            return ''
        return year
    get_year.short_description = _('Year')


@admin.register(FS_LoB)
class FS_LoBAdmin(admin.ModelAdmin):
    ordering = ('quarter__year__company__corp_name', )
    list_display = (
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'unit', 'exist', 'ROE', 'ROA', 'GPA', 'net_income', 'total_capital', 
    )
    list_display_links = (
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'unit', 'exist', 'ROE', 'ROA', 'GPA', 'net_income', 'total_capital', 
    )
    search_fields = (
        'quarter__year__company__corp_name', 'quarter__year__bs_year', 'quarter__qt_name',
        'lob', 'unit', 'exist',
    )
    list_filter = ('lob', 'exist', 'unit', )
    
    list_select_related = [
        'quarter',
        'quarter__year',
        'quarter__year__company',
    ]
    
    inlines = ()
    
    def get_lob(self, obj):
        lob = obj.lob
        return lob
    get_lob.short_description = _('Linked or Basic')
    
    def get_quarter(self, obj):
        if obj.quarter.qt_name == "11013":
            return "1??????"
        elif obj.quarter.qt_name == "11012":
            return "2??????"
        elif obj.quarter.qt_name == "11014":
            return "3?????? ?????????"
        elif obj.quarter.qt_name == "11011":
            return "?????? ?????????"
        else:
            return ''
    get_quarter.short_description = _('Quarter')
    
    def get_company(self, obj):
        company = obj.quarter.year.company.corp_name
        
        if not company:
            return ''
        return company
    get_company.short_description = _('Company')
    
    def get_year(self, obj):
        year = obj.quarter.year.bs_year
        
        if not year:
            return ''
        return year
    get_year.short_description = _('Year')
    


@admin.register(FS_Div)
class FS_DivAdmin(admin.ModelAdmin):
    ordering = ('lob__quarter__year__company__corp_name', )
    list_display = (
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'get_fsdiv',
    )
    list_display_links = (
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'get_fsdiv',
    )
    search_fields = (
        'fs_lob__quarter__year__company__corp_name', 
        'fs_lob__quarter__year__bs_year', 'fs_lob__quarter__qt_name', 
        'fs_lob__lob', 'sj_div',
    )
    list_filter = ()
    
    list_select_related = [
        'lob',
        'lob__quarter',
        'lob__quarter__year',
        'lob__quarter__year__company',
    ]
    
    inlines = ()
    
    def get_fsdiv(self, obj):
        if obj.sj_div == "BS":
            return "???????????????"
        elif obj.sj_div == "IS": 
            return "???????????????"
        elif obj.sj_div == "CIS": 
            return "?????????????????????"
        elif obj.sj_div == "CF": 
            return "???????????????"
        elif obj.sj_div == "SCE":
            return "???????????????"
    get_fsdiv.short_description = _('FS_Div')
    
    
    def get_lob(self, obj):
        lob = obj.lob.lob
        return lob
    get_lob.short_description = _('Linked or Basic')
    
    
    def get_quarter(self, obj):
        if obj.lob.quarter.qt_name == "11013":
            return "1??????"
        elif obj.lob.quarter.qt_name == "11012":
            return "2??????"
        elif obj.lob.quarter.qt_name == "11014":
            return "3?????? ?????????"
        elif obj.lob.quarter.qt_name == "11011":
            return "?????? ?????????"
        else:
            return ''
    get_quarter.short_description = _('Quarter')
    
    def get_company(self, obj):
        company = obj.lob.quarter.year.company.corp_name
        
        if not company:
            return ''
        return company
    get_company.short_description = _('Company')
    
    def get_year(self, obj):
        year = obj.lob.quarter.year.bs_year
        
        if not year:
            return ''
        return year
    get_year.short_description = _('Year')


@admin.register(FS_Account)
class FS_AccountAdmin(admin.ModelAdmin):
    ordering = ('fs_div__lob__quarter__year__company__corp_name', )
    list_display = (
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'get_fsdiv', 'account_name', 'account_amount',
        'get_unit',
    )
    list_display_links = (
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'get_fsdiv','account_name', 'account_amount',
        'get_unit',
    )
    search_fields = (
        'fs_div__lob__quarter__year__company__corp_name', 
        'fs_div__lob__quarter__year__bs_year', 
        'fs_div__lob__quarter__qt_name', 
        'fs_div__lob__lob', 'fs_div__sj_div', 'account_name',
    )
    # list_filter = ('account_name', )
    
    list_select_related = [
        'fs_div',
        'fs_div__lob',
        'fs_div__lob__quarter',
        'fs_div__lob__quarter__year',
        'fs_div__lob__quarter__year__company',
    ]
    
    inlines = ()
    
    def get_unit(self, obj):
        unit = obj.fs_div.lob.unit
        return unit
    get_unit.short_description = _('Unit')
    
    def get_fsdiv(self, obj):
        if obj.fs_div.sj_div == "BS":
            return "???????????????"
        elif obj.fs_div.sj_div == "IS": 
            return "???????????????"
        elif obj.fs_div.sj_div == "CIS": 
            return "?????????????????????"
        elif obj.fs_div.sj_div == "CF": 
            return "???????????????"
        elif obj.fs_div.sj_div == "SCE":
            return "???????????????"
    get_fsdiv.short_description = _('FS_Div')
    
    
    def get_lob(self, obj):
        lob = obj.fs_div.lob.lob
        return lob
    get_lob.short_description = _('Linked or Basic')
    
    
    def get_quarter(self, obj):
        if obj.fs_div.lob.quarter.qt_name == "11013":
            return "1??????"
        elif obj.fs_div.lob.quarter.qt_name == "11012":
            return "2??????"
        elif obj.fs_div.lob.quarter.qt_name == "11014":
            return "3?????? ?????????"
        elif obj.fs_div.lob.quarter.qt_name == "11011":
            return "?????? ?????????"
        else:
            return ''
    get_quarter.short_description = _('Quarter')
    
    def get_company(self, obj):
        company = obj.fs_div.lob.quarter.year.company.corp_name
        
        if not company:
            return ''
        return company
    get_company.short_description = _('Company')
    
    def get_year(self, obj):
        year = obj.fs_div.lob.quarter.year.bs_year
        
        if not year:
            return ''
        return year
    get_year.short_description = _('Year')


@admin.register(SUB_Account)
class SUB_AccountAdmin(admin.ModelAdmin):
    ordering = ('pre_account__fs_div__lob__quarter__year__company__corp_name', )
    list_display = (
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'get_fsdiv', 'get_fs_account', 'account_name', 'account_amount',
        'get_unit',
    )
    list_display_links = (
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'get_fsdiv','get_fs_account', 'account_name', 'account_amount',
        'get_unit',
    )
    search_fields = (
        'fs_account__fs_div__fs_lob__quarter__year__company__corp_name', 
        'account_name',
        'unit',
    )
    # list_filter = ('account_name', )
    
    list_select_related = [
        'pre_account',
        'pre_account__fs_div',
        'pre_account__fs_div__lob',
        'pre_account__fs_div__lob__quarter',
        'pre_account__fs_div__lob__quarter__year',
        'pre_account__fs_div__lob__quarter__year__company',
    ]
    
    inlines = ()
    
    def get_unit(self, obj):
        unit = obj.pre_account.fs_div.lob.unit
        return unit
    get_unit.short_description = _('Unit')
    
    def get_fs_account(self, obj):
        preaccount = obj.pre_account.account_name
        return preaccount
    get_fs_account.short_description = _('FS_Account')
    
    def get_fsdiv(self, obj):
        if obj.pre_account.fs_div.sj_div == "BS":
            return "???????????????"
        elif obj.pre_account.fs_div.sj_div == "IS": 
            return "???????????????"
        elif obj.pre_account.fs_div.sj_div == "CIS": 
            return "?????????????????????"
        elif obj.pre_account.fs_div.sj_div == "CF": 
            return "???????????????"
        elif obj.pre_account.fs_div.sj_div == "SCE":
            return "???????????????"
    get_fsdiv.short_description = _('FS_Div')
    
    
    def get_lob(self, obj):
        lob = obj.pre_account.fs_div.lob.lob
        return lob
    get_lob.short_description = _('Linked or Basic')
    
    
    def get_quarter(self, obj):
        if obj.pre_account.fs_div.lob.quarter.qt_name == "11013":
            return "1??????"
        elif obj.pre_account.fs_div.lob.quarter.qt_name == "11012":
            return "2??????"
        elif obj.pre_account.fs_div.lob.quarter.qt_name == "11014":
            return "3?????? ?????????"
        elif obj.pre_account.fs_div.lob.quarter.qt_name == "11011":
            return "?????? ?????????"
        else:
            return ''
    get_quarter.short_description = _('Quarter')
    
    def get_company(self, obj):
        company = obj.pre_account.fs_div.lob.quarter.year.company.corp_name
        
        if not company:
            return ''
        return company
    get_company.short_description = _('Company')
    
    def get_year(self, obj):
        year = obj.pre_account.fs_div.lob.quarter.year.bs_year
        
        if not year:
            return ''
        return year
    get_year.short_description = _('Year')
    
    
@admin.register(Daily_Price)
class Daily_PriceAdmin(admin.ModelAdmin):
    ordering = ('date', )
    list_display = (
        'get_company', 'date', 'open', 'close',
        'low', 'high', 'volume', 'per', 'pbr'
    )
    list_display_links = (
        'get_company', 'date', 'open', 'close',
        'low', 'high', 'volume', 'per', 'pbr'
    )
    search_fields = (
        'company__corp_name',
    )
    
    inlines = ()
    list_select_related = [
        'company'
    ]
    
    def get_company(self, obj):
        company = obj.company.corp_name
        
        if not company:
            return ''
        return company
    get_company.short_description = _('Company')
    