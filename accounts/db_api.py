from accounts.models import CustomUser
from rest_framework.authtoken.models import Token

def get_customuser(*args,**kwargs) -> CustomUser:
    return CustomUser.objects.get(*args,**kwargs)

def create_customuser(*args,**kwargs) -> CustomUser:
    return CustomUser.objects.create_user(*args,**kwargs)

def get_or_create_token(*args,**kwargs) -> Token:
    return Token.objects.get_or_create(*args,**kwargs)