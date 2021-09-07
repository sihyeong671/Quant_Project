from rest_framework import serializers

from stockmanage.models import Company


class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = '__all__'
        
