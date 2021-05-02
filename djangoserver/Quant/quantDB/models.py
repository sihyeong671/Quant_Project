from django.db import models

class Quarter(models.Model):
    stock_date = models.DateField(auto_now=False, auto_now_add=False)
    benefit = models.IntegerField()
    

class Financial_Statements(models.Model):
    quarter = models.ForeignKey(Quarter, on_delete=models.CASCADE)

    
class Company(models.Model):
    company_name = models.CharField(max_length=200, null=False)
    fs = models.ForeignKey(Financial_Statements, on_delete=models.CASCADE)
