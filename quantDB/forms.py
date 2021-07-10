from django import forms
from quantDB.models import Company


class StockForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name']
        labels = {
            'company_name': '이름'
        }