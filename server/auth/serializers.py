from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

from users.models import User


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, write_only=True)
    email = serializers.EmailField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError(
                _("email field not allowed empty")
            )
        used = User.objects.filter(email__iexact=email)
        if used.count() > 0:
            raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        
        return email
    
    def validate_password12(self, password1, password2):
        if not password1 or not password2:
            raise serializers.ValidationError(
                _("need two password fields")
            )
        if password1 != password2:
            raise serializers.ValidationError(_("password fields didn't match!"))
        
        return password1
    
    def validate_username(self, username):
        print("check validate username")
        if not username:
            raise serializers.ValidationError(
                _("username field not allowed empty")
            )
        used = User.objects.filter(username__iexact=username).first()
        if used:
            raise serializers.ValidationError(
                    _("A user is already registered with this username."))
        
        return username
    
    def validate(self, data):
        print("check validate ALL")
        
        data['password1'] = self.validate_password12(data['password1'], data['password2'])
        data['email'] = self.validate_email(data['email'])
        data['username'] = self.validate_username(data['username'])
        
        return data

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password1"]
        )
        
        return user
