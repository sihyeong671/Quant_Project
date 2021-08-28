from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.management.utils import get_random_secret_key
from django.utils.translation import gettext_lazy as _
from django.core import validators
from django.utils.deconstruct import deconstructible

from boards.models import Post
from DBmanageapp.models import Company

@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+\Z'
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers, and @/./+/-/_ characters.'
    )
    flags = 0


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        print("Create User by manager")
        if not username:
            raise ValueError('아이디는 필수 항목입니다.')
        if not email:
            raise ValueError('이메일은 필수 항목입니다.')
        if not password:
            raise ValueError('패드워드는 필수 항목입니다,')
        
        
        user = self.model(
            username=username,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.full_clean()
        user.save()
        
        profile = Profile(user=user, nickname=username)
        profile.save()
        
        return user
    
    def create_superuser(self, username, email=None, password=None):
        
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=True
    )
    secret_key = models.CharField(
        max_length=255,
        default=get_random_secret_key()
    )
    
    object = UserManager()
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        
    def __str__(self):
        return self.username
    

    @property
    def name(self):
        if not self.last_name:
            return self.first_name.capitalize()

        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    auth = models.CharField(max_length=128, null=True, blank=True)
    nickname = models.CharField(max_length=64, unique=True)
    image = models.ImageField(
        default='profile_image/basic_profile.png',
        upload_to='profile_image/',
        null=True, blank=True
    )
    introduce = models.TextField(null=True, blank=True)
    
    signup_path = models.CharField(max_length=64, default='basic')
    
    favorite_company = models.ManyToManyField(Company)
    favorite_post = models.ManyToManyField(Post)
    
    def __str__(self):
        return self.user.username
    
