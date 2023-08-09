from rest_framework import serializers
from .models import ExpiringToken

class ExpiringTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringToken
        fields = ('key', 'user', 'expiration')
