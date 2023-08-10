from rest_framework import serializers
from .models import ExpiringToken,LabUser,PatientUser

class ExpiringTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringToken
        fields = ('key', 'user', 'expiration')

class LabUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabUser
        fields = '__all__'

class PatientUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientUser
        fields = '__all__'
