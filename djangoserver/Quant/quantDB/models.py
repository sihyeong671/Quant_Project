from django.db import models

# items = ["rcept_no","reprt_code","bsns_year","sj_div","sj_nm","account_nm","account_detail","thstrm_amount"]
# item_names = ["접수번호","보고서코드","사업연도","재무제표구분","재무제표명","계정명","계정상세","당기금액"]

# 객체 n개
class Company(models.Model):
    company_name = models.CharField(max_length=200, null=False)
    
    class Meta:
        # admin 페이지에서 조회할 때, 클래스명 대신 알아보기 쉬운 단어로 지정하는 것
        verbose_name = "기업"
        ordering = ["company_name"]

# 객체 7개 (2015 ~ 2017)
class Year(models.Model):
    bsns_year = models.IntegerField(help_text="사업연도", blank=True, null=True)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "연도별 데이터"

# 객체 4개 (1/4, 2/4, 3/4, 4/4)
class Quarter(models.Model):
    # report_code = models.IntegerField(help_text="보고서코드(분기 구분)", blank=False, null=False)  # 분기를 판단
    quarter_name = models.CharField(help_text="분기", max_length=30, blank=True, null=True)
    year = models.ForeignKey(Year, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "분기별 데이터"
        ordering = ["account_name"]

# 객체 2개 (linked or basic)
class Financial_Statements_LinkOrBasic(models.Model):
    linkOrbasic = models.CharField(max_length=30, blank=True, null=True)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "연결/기본"

# 객체 5개 (BS:재무상태표, IS:손익계산서, CIS:포괄손익계산서, CF:현금흐름표, SCE:자본변동표)
class Financial_Statements_Div(models.Model):
    # sj_name = models.CharField(help_text="재무제표명(재무상태표 손익계산서...)", max_length=255, blank=False, null=False)
    sj_div = models.CharField(help_text="재무제표구분(BS IS ...)", max_length=255, blank=False, null=False)
    lb = models.ForeignKey(Financial_Statements_LinkOrBasic, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "재무제표구분"

class FS_Account(models.Model):
    financial_statements_div = models.ForeignKey(Financial_Statements_Div, on_delete=models.CASCADE)
    account_name = models.CharField(help_text="계정명", max_length=255, blank=False, null=False)
    a = models.IntegerField(help_text="계정명에 대한 자산", blank=True, null=True)
