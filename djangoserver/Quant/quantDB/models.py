from django.db import models

class Quarter(models.Model):
    stock_date = models.DateField(auto_now=False, auto_now_add=False)
    benefit = models.IntegerField()
    
    class Meta:
        verbose_name = "분기별 데이터"
        ordering = ["stock_date"]
    

class Financial_Statements(models.Model):
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "재무재표"

    
class Company(models.Model):
    company_name = models.CharField(max_length=200, null=False)
    fs = models.ForeignKey(Financial_Statements, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "기업 이름"
        ordering = ["company_name"]