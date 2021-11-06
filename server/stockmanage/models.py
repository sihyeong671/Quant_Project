from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Company(models.Model):
    corp_name = models.CharField(max_length=100, null=True, blank=True)
    corp_name_eng = models.CharField(max_length=100, null=True, blank=True)
    stock_name = models.CharField(max_length=100, null=True, blank=True)
    stock_code = models.CharField(max_length=100, null=True, blank=True)
    ceo_name = models.CharField(max_length=100, null=True, blank=True)
    # 법인구분 Y:유가, K:코스닥, N:코넥스, E:기타
    corp_cls = models.CharField(max_length=100, null=True, blank=True)
    jurir_no = models.CharField(max_length=100, null=True, blank=True)
    bizr_no = models.CharField(max_length=100, null=True, blank=True)
    adres = models.CharField(max_length=100, null=True, blank=True)
    hm_url = models.CharField(max_length=100, null=True, blank=True)
    ir_url = models.CharField(max_length=100, null=True, blank=True)
    phn_no = models.CharField(max_length=100, null=True, blank=True)
    fax_no = models.CharField(max_length=100, null=True, blank=True)
    # 업종코드
    induty_code = models.CharField(max_length=100, null=True, blank=True)
    est_dt = models.CharField(max_length=100, null=True, blank=True)
    # 결산월
    acc_mt = models.CharField(max_length=100, null=True, blank=True)

    
    def __str__(self):
        return self.corp_name
    
    class Meta:
        # admin 페이지에서 조회할 때, 클래스명 대신 알아보기 쉬운 단어로 지정하는 것
        verbose_name = "기업"
        verbose_name_plural = "기업"
        ordering = ["corp_name"]


class Daily_Price(models.Model):
    # 날짜 문자열로 저장
    date = models.DateField(null=True, blank=True)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)

    market_gap = models.FloatField(help_text="시가총액", null=True, blank=True)
    # per = models.FloatField(help_text="PER", null=True, blank=True)
    # pbr = models.FloatField(help_text="PBR", null=True, blank=True)

    open = models.FloatField(help_text="시가", null=True, blank=True)
    high = models.FloatField(help_text="고가", null=True, blank=True)
    low = models.FloatField(help_text="저가", null=True, blank=True)
    close = models.FloatField(help_text="종가", null=True, blank=True)
    volume = models.FloatField(help_text="거래량", null=True, blank=True)

    def __str__(self):
        return str(self.date)
    
    class Meta:
        verbose_name = "일별 데이터"
        verbose_name_plural = "일별 데이터"


# 객체 7개 (2015 ~ 2017)
class Year(models.Model):
    bs_year = models.IntegerField(help_text="사업연도", blank=True, null=True)
    company = models.ForeignKey(
        Company,
        null=True, blank=True, 
        on_delete=models.CASCADE, related_name = 'year'
    )
    
    def __str__(self):
        return str(self.bs_year)
    
    class Meta:
        verbose_name = "연도별 데이터"
        verbose_name_plural = "연도별 데이터"


# 객체 4개 (1/4, 2/4, 3/4, 4/4)
class Quarter(models.Model):
    qt_name = models.CharField(
        help_text="1분기:11013 2분기:11012 3분기보고서:11014 사업보고서:11011",
        max_length=30, blank=True, null=True
    )
    year = models.ForeignKey(
        Year,
        null=True, blank=True,
        on_delete=models.CASCADE, related_name='quarter'
    )
    
    def __str__(self):
        return self.qt_name
    
    class Meta:
        verbose_name = "분기별 데이터"
        verbose_name_plural = "분기별 데이터"


# 객체 2개 (linked or basic)
# 연결/일반 재무제표 구분
class FS_LoB(models.Model):
    lob = models.CharField(help_text="연결(CFS)/일반(OFS)", max_length=30, blank=True, null=True)
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE, related_name="fs_lob")
    exist = models.IntegerField(default=0, null=True, blank=True)
    # 돈 단위 - api에서 받는거랑 다를 수도 있음
    unit = models.CharField(max_length=30, null=True, blank=True)
    ROA = models.FloatField(null=True, blank=True)
    ROE = models.FloatField(null=True, blank=True)

    # 부채비율
    # 기업가치
    # EBIT
    # EBIDTA



    def __str__(self):
        return self.lob
    
    class Meta:
        verbose_name = "연결/일반"
        verbose_name_plural = "연결/일반"


# 객체 5개 (BS:재무상태표, IS:손익계산서, CIS:포괄손익계산서, CF:현금흐름표, SCE:자본변동표)
class FS_Div(models.Model):
    sj_div = models.CharField(
        help_text="재무제표구분(BS:재무상태표, IS:손익계산서, CIS:포괄손익계산서, CF:현금흐름표, SCE:자본변동표)",
        max_length=255, 
        blank=True, null=True
    )
    lob = models.ForeignKey(FS_LoB, on_delete=models.CASCADE, related_name='fs_div')
    
    def __str__(self):
        return self.sj_div
        
    class Meta:
        verbose_name = "재무제표구분"
        verbose_name_plural = "재무제표구분"


class FS_Account(models.Model):
    fs_div = models.ForeignKey(FS_Div, on_delete=models.CASCADE, related_name="fs_account", null=True)
    account_name = models.CharField(help_text="계정명", max_length=255, blank=True, null=True)
    account_amount = models.FloatField(help_text="계정명에 대한 자산", blank=True, null=True)
    account_add_amount = models.FloatField(help_text="계정명에 대한 누적 금액", blank=True, null=True)
    account_detail = models.CharField(help_text="계정상세", max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.account_name

    class Meta:
        verbose_name = "계정명"
        verbose_name_plural = "계정명"


class SUB_Account(models.Model):
    pre_account = models.ForeignKey(FS_Account, on_delete=models.CASCADE, related_name="sub_account")
    account_name = models.CharField(help_text="계정명", max_length=255, blank=True, null=True)
    account_amount = models.FloatField(help_text="계정명에 대한 금액", blank=True, null=True)
    account_add_amount = models.FloatField(help_text="계정명에 대한 누적 금액", blank=True, null=True)
    account_detail = models.CharField(help_text="계정상세", max_length=255, blank=True, null=True)
    def __str__(self):
        return self.account_name

    class Meta:
        verbose_name = "sub계정명"
        verbose_name_plural = "sub계정명"


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


class UserCustomBS(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_bs')
    custom_title = models.CharField(max_length=100, null=True, blank=True)
    stock_code = models.CharField(max_length=100, null=True, blank=True)
    bs_year = models.IntegerField(help_text="사업연도", blank=True, null=True)
    qt_name = models.CharField(
        help_text="1분기:11013 2분기:11012 3분기보고서:11014 사업보고서:11011",
        max_length=30, blank=True, null=True
    )
    lob = models.CharField(help_text="연결(CFS)/일반(OFS)", max_length=30, blank=True, null=True)
    sj_div = models.CharField(
        help_text="재무제표구분(BS:재무상태표, IS:손익계산서, CIS:포괄손익계산서, CF:현금흐름표, SCE:자본변동표)",
        max_length=255, 
        blank=True, null=True
    )


class CustomFS_Account(models.Model):
    custom_bs = models.ForeignKey(UserCustomBS, on_delete=models.CASCADE, related_name="fs_account")
    account_name = models.CharField(help_text="계정명", max_length=255, blank=True, null=True)
    account_amount = models.FloatField(help_text="계정명에 대한 자산", blank=True, null=True)
    coef = models.IntegerField(default=1, null=True, blank=True)


class CustomSUB_Account(models.Model):
    pre_account = models.ForeignKey(CustomFS_Account, on_delete=models.CASCADE, related_name="sub_account")
    account_name = models.CharField(help_text="계정명", max_length=255, blank=True, null=True)
    account_amount = models.FloatField(help_text="계정명에 대한 금액", blank=True, null=True)
    coef = models.IntegerField(default=1, null=True, blank=True)

