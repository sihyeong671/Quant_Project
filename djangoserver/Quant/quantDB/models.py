from django.db import models

# items = ["rcept_no","reprt_code","bsns_year","sj_div","sj_nm","account_nm","account_detail","thstrm_amount"]
# item_names = ["접수번호","보고서코드","사업연도","재무제표구분","재무제표명","계정명","계정상세","당기금액"]

class Company(models.Model):
    company_name = models.CharField(max_length=200, null=False)
    
    class Meta:
        # admin 페이지에서 조회할 때, 클래스명 대신 알아보기 쉬운 단어로 지정하는 것
        verbose_name = "기업"
        ordering = ["company_name"]

class Financial_Statements(models.Model):
    sj_name = models.CharField(help_text="제무제표명", max_length=255, blank=False, null=False)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "재무재표명"

class Year(models.Model):
    bsns_year = models.IntegerField(help_text="사업연도", blank=False, null=False)
    financial_statements = models.ForeignKey(Financial_Statements, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "연도별 데이터"

class Quarter(models.Model):
    # report_code = models.IntegerField(help_text="보고서코드(분기 구분)", blank=False, null=False)  # 분기를 판단
    
    quarter_name = models.CharField(help_text="분기", max_length=30, blank=True, null=True)
    sj_div = models.CharField(help_text="제무제표구분", max_length=255, blank=False, null=False)
    sj_name = models.CharField(help_text="제무제표명", max_length=255, blank=False, null=False)
    account_name = models.CharField(help_text="계정명", max_length=255, blank=False, null=False)
    account_detail = models.CharField(help_text="계정상세", max_length=255, blank=False, null=False)
    thstrm_amount = models.IntegerField(help_text="당기금액", blank=False, null=False)
    
    year = models.ForeignKey(Year, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "분기별 데이터"
        ordering = ["account_name"]
