from django.db import models

# items = ["rcept_no","reprt_code","bsns_year","sj_div","sj_nm","account_nm","account_detail","thstrm_amount"]
# item_names = ["접수번호","보고서코드","사업연도","재무제표구분","재무제표명","계정명","계정상세","당기금액"]

# 객체 n개

class Company(models.Model):
    company_name = models.CharField(max_length=200, null=False)
    short_code = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.company_name
    
    class Meta:
        # admin 페이지에서 조회할 때, 클래스명 대신 알아보기 쉬운 단어로 지정하는 것
        verbose_name = "기업"
        verbose_name_plural = "기업"
        ordering = ["company_name"]

# 객체 7개 (2015 ~ 2017)
class Year(models.Model):
    bs_year = models.IntegerField(help_text="사업연도", blank=True, null=True)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.bs_year)
    
    class Meta:
        verbose_name = "연도별 데이터"
        verbose_name_plural = "연도별 데이터"

# 객체 4개 (1/4, 2/4, 3/4, 4/4)
class Quarter(models.Model):
    qt_name = models.CharField(help_text="1분기:11013 2분기:11012 3분기보고서:11014 사업보고서:11011",\
        max_length=30, blank=True, null=True)
    year = models.ForeignKey(Year, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.qt_name
    
    class Meta:
        verbose_name = "분기별 데이터"
        verbose_name_plural = "분기별 데이터"

# 객체 2개 (linked or basic)
# 연결/일반 재무제표 구분
class FS_LoB(models.Model):
    lob = models.CharField(help_text="연결/일반", max_length=30, blank=True, null=True)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.lob
    
    class Meta:
        verbose_name = "연결/일반"
        verbose_name_plural = "연결/일반"

# 객체 5개 (BS:재무상태표, IS:손익계산서, CIS:포괄손익계산서, CF:현금흐름표, SCE:자본변동표)
class FS_Div(models.Model):
    sj_div = models.CharField(help_text="재무제표구분(BS:재무상태표, IS:손익계산서, CIS:포괄손익계산서, CF:현금흐름표, SCE:자본변동표)",\
         max_length=255, blank=True, null=True)
    lob = models.ForeignKey(FS_LoB, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.sj_div
        
    class Meta:
        verbose_name = "재무제표구분"
        verbose_name_plural = "재무제표구분"

class FS_Account(models.Model):
    fs_div = models.ForeignKey(FS_Div, on_delete=models.CASCADE)
    account_name = models.CharField(help_text="계정명", max_length=255, blank=True, null=True)
    account_amount = models.FloatField(help_text="계정명에 대한 자산", blank=True, null=True)
    account_detail = models.CharField(help_text="계정상세", max_length=255, blank=True, null=True)
    def __str__(self):
        return self.account_name

    class Meta:
        verbose_name = "계정명"
        verbose_name_plural = "계정명"

class SUB_Account(models.Model):
    fs_div = models.ForeignKey(FS_Account, on_delete=models.CASCADE)
    account_name = models.CharField(help_text="계정명", max_length=255, blank=True, null=True)
    account_amount = models.FloatField(help_text="계정명에 대한 자산", blank=True, null=True)
    account_detail = models.CharField(help_text="계정상세", max_length=255, blank=True, null=True)
    def __str__(self):
        return self.account_name

    class Meta:
        verbose_name = "계정명"
        verbose_name_plural = "계정명"

class Dart(models.Model):
    dart_code = models.CharField(help_text="고유번호",max_length=10, blank=True, null=True)
    company_name_dart = models.CharField(help_text="회사명",max_length=50,blank=True, null=True)
    short_code = models.CharField(help_text="종목코드",max_length=30,blank=True, null=True)
    recent_modify = models.CharField(help_text="최종변경일자", max_length=30,blank=True, null=True)
    
    def __str__(self):
        return self.company_name_dart

    class Meta:
        verbose_name = "dart info"
        verbose_name_plural = "dart info"

class Corpdata(models.Model):
    market_cap = models.IntegerField(help_text="시가총액", null=True, blank=True)
    per = models.FloatField(help_text="PER", null=True, blank=True)
    pbr = models.FloatField(help_text="PBR", null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "일별 데이터"
        verbose_name_plural = "일별 데이터"
