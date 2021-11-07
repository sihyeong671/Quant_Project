from rest_framework import serializers

from stockmanage.models import Company, UserCustomBS, CustomFS_Account, CustomSUB_Account


class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = '__all__'
        

class CustomSUB_AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomSUB_Account
        fields = '__all__'
        
        
class CustomFS_AccountSerializer(serializers.ModelSerializer):
    sub_account = CustomSUB_AccountSerializer(many=True)
    
    class Meta:
        model = CustomFS_Account
        fields = '__all__'


class UserCustomBSSerializer(serializers.ModelSerializer):
    fs_account = CustomFS_AccountSerializer(many=True)
    
    class Meta:
        model = UserCustomBS
        fields = '__all__'
    


