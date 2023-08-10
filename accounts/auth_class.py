from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from .models import ExpiringToken

class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = ExpiringToken.objects.get(key=key)
        except ExpiringToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if token.expiration < timezone.now():
            token.delete()
            raise AuthenticationFailed('Token has expired')
        
        return (token.user, token.key)
