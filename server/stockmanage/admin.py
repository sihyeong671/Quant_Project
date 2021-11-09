from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from stockmanage.models import *



# admin.site.register(Dart)
# admin.site.register(Company)
# admin.site.register(Year)
# admin.site.register(Quarter)
# admin.site.register(FS_LoB)
# admin.site.register(FS_Div)
# admin.site.register(FS_Account)
# admin.site.register(SUB_Account)
admin.site.register(Daily_Price)


@admin.register(Dart)
class CompanyAdmin(admin.ModelAdmin):
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
    search_fields = ('get_company', 'bs_year',)
    list_filter = ('bs_year', )
    
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
        # 'ROE', 'ROA',
    )
    list_display_links = (
        'get_company', 'get_year', 'get_quarter', 
        # 'ROE', 'ROA',
    )
    search_fields = (
        'get_company', 'get_year', 'get_quarter', 
        # 'ROE', 'ROA',
    )
    list_filter = ('qt_name', )
    
    inlines = ()
    
    def get_quarter(self, obj):
        if obj.qt_name == "11013":
            return "1분기"
        elif obj.qt_name == "11012":
            return "2분기"
        elif obj.qt_name == "11014":
            return "3분기 보고서"
        elif obj.qt_name == "11011":
            return "사업 보고서"
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
        'get_lob', 'unit','exist'
    )
    list_display_links = (
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'unit','exist'
    )
    search_fields = (
        'get_company', 'get_year', 'get_quarter',
        'get_lob', 'unit','exist'
    )
    list_filter = ('lob', 'exist', 'unit', )
    
    inlines = ()
    
    def get_lob(self, obj):
        lob = obj.lob
        return lob
    get_lob.short_description = _('Linked or Basic')
    
    def get_quarter(self, obj):
        if obj.quarter.qt_name == "11013":
            return "1분기"
        elif obj.quarter.qt_name == "11012":
            return "2분기"
        elif obj.quarter.qt_name == "11014":
            return "3분기 보고서"
        elif obj.quarter.qt_name == "11011":
            return "사업 보고서"
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
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'get_fsdiv',
    )
    list_filter = ('sj_div', )
    
    inlines = ()
    
    def get_fsdiv(self, obj):
        if obj.sj_div == "BS":
            return "재무상태표"
        elif obj.sj_div == "IS": 
            return "손익계산서"
        elif obj.sj_div == "CIS": 
            return "포괄손익계산서"
        elif obj.sj_div == "CF": 
            return "현금흐름표"
        elif obj.sj_div == "SCE":
            return "자본변동표"
    get_fsdiv.short_description = _('FS_Div')
    
    
    def get_lob(self, obj):
        lob = obj.lob.lob
        return lob
    get_lob.short_description = _('Linked or Basic')
    
    
    def get_quarter(self, obj):
        if obj.lob.quarter.qt_name == "11013":
            return "1분기"
        elif obj.lob.quarter.qt_name == "11012":
            return "2분기"
        elif obj.lob.quarter.qt_name == "11014":
            return "3분기 보고서"
        elif obj.lob.quarter.qt_name == "11011":
            return "사업 보고서"
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
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'get_fsdiv','account_name',
    )
    list_filter = ('account_name', )
    
    inlines = ()
    
    def get_unit(self, obj):
        unit = obj.fs_div.lob.unit
        return unit
    get_unit.short_description = _('Unit')
    
    def get_fsdiv(self, obj):
        if obj.fs_div.sj_div == "BS":
            return "재무상태표"
        elif obj.fs_div.sj_div == "IS": 
            return "손익계산서"
        elif obj.fs_div.sj_div == "CIS": 
            return "포괄손익계산서"
        elif obj.fs_div.sj_div == "CF": 
            return "현금흐름표"
        elif obj.fs_div.sj_div == "SCE":
            return "자본변동표"
    get_fsdiv.short_description = _('FS_Div')
    
    
    def get_lob(self, obj):
        lob = obj.fs_div.lob.lob
        return lob
    get_lob.short_description = _('Linked or Basic')
    
    
    def get_quarter(self, obj):
        if obj.fs_div.lob.quarter.qt_name == "11013":
            return "1분기"
        elif obj.fs_div.lob.quarter.qt_name == "11012":
            return "2분기"
        elif obj.fs_div.lob.quarter.qt_name == "11014":
            return "3분기 보고서"
        elif obj.fs_div.lob.quarter.qt_name == "11011":
            return "사업 보고서"
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
        'get_company', 'get_year', 'get_quarter', 
        'get_lob', 'get_fsdiv','get_fs_account', 'account_name', 'account_amount',
        'get_unit',

    )
    list_filter = ('account_name', )
    
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
            return "재무상태표"
        elif obj.pre_account.fs_div.sj_div == "IS": 
            return "손익계산서"
        elif obj.pre_account.fs_div.sj_div == "CIS": 
            return "포괄손익계산서"
        elif obj.pre_account.fs_div.sj_div == "CF": 
            return "현금흐름표"
        elif obj.pre_account.fs_div.sj_div == "SCE":
            return "자본변동표"
    get_fsdiv.short_description = _('FS_Div')
    
    
    def get_lob(self, obj):
        lob = obj.pre_account.fs_div.lob.lob
        return lob
    get_lob.short_description = _('Linked or Basic')
    
    
    def get_quarter(self, obj):
        if obj.pre_account.fs_div.lob.quarter.qt_name == "11013":
            return "1분기"
        elif obj.pre_account.fs_div.lob.quarter.qt_name == "11012":
            return "2분기"
        elif obj.pre_account.fs_div.lob.quarter.qt_name == "11014":
            return "3분기 보고서"
        elif obj.pre_account.fs_div.lob.quarter.qt_name == "11011":
            return "사업 보고서"
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