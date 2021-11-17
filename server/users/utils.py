from django.core.management.utils import get_random_secret_key
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

from users.models import Profile

User = get_user_model()

@transaction.atomic
def user_create(username, password=None, **extra_fields):
    user = User(username=username, email=username)
    
    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()
        
    user.full_clean()
    user.save()
    
    profile = Profile(user=user)
    
    try:
        profile.image = extra_fields['image']
    except:
        pass
    
    try:
        if extra_fields['nickname']:
            profile.nickname = extra_fields['nickname']
        else:
            profile.nickname = username
    except:
        pass
    
    try:
        try:
            user.first_name = extra_fields['first_name']
            user.last_name = extra_fields['last_name']
        except:
            try:
                user.first_name = extra_fields['name']
            except:
                pass
    except:
        pass
    
    try:
        path = extra_fields['path']
        profile.signup_path = f"{path}"
        profile.image = f"profile_image/{path}_basic.png"
    except:
        pass
    
    profile.save()
    
    return user


def user_create_superuser(username, password=None, **extra_fields):
    extra_fields = {
        'is_staff': True,
        'is_superuser': True,
        **extra_fields
    }
    
    user = user_create(username=username, password=password, extra_fields=extra_fields)
    
    return user


def user_record_login(user: User):
    user.last_login = timezone.now()
    user.save()
    
    return user


@transaction.atomic
def user_get_or_create(username, **extra_data):
    user = User.objects.filter(email=username).first()
    
    if user:
        return user, False
    
    return user_create(username=username, **extra_data), True

