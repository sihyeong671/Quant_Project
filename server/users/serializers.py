from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from users.models import User, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'image',
            'introduce',
            'signup_path'
        ]

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'profile',
            'last_login',
            'date_joined',
        ]


class PasswordChangeSerializer(serializers.Serializer):
    oldpassword = serializers.CharField(write_only=True)
    newpassword1 = serializers.CharField(write_only=True)
    newpassword2 = serializers.CharField(write_only=True)
    
    def validate_password(self, oldpassword, newpassword1, newpassword2):
        if oldpassword == newpassword1 or oldpassword == newpassword2:
            raise serializers.ValidationError(
                _("oldpw and newpw are same either"))
        if not newpassword1 or not newpassword2:
            raise serializers.ValidationError(
                _("need two password fields"))
        if newpassword1 != newpassword2:
            raise serializers.ValidationError(_("password fields didn't match!"))
        
        return newpassword1
    
    def validate(self, data):
        data['newpassword1'] = self.validate_password(
            data['oldpassword'], data['newpassword1'], data['newpassword2'])
        
        return data
    
    def update(self, user, validated_data):
        user.set_password(validated_data.get('newpassword1'))
        user.save()
        
        return user