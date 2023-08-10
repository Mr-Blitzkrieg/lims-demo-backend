from accounts.models import CustomUser,LabUser,PatientUser
from .models import ExpiringToken
from django.db.models import QuerySet

def get_customuser(*args,**kwargs) -> CustomUser:
    return CustomUser.objects.get(*args,**kwargs)

def create_customuser(*args,**kwargs) -> CustomUser:
    return CustomUser.objects.create_user(*args,**kwargs)

def get_or_create_token(*args,**kwargs) -> ExpiringToken:
    return ExpiringToken.objects.get_or_create(*args,**kwargs)

def get_all_labuser() -> QuerySet:
    return LabUser.objects.all()

def create_labuser(*args,**kwargs) -> LabUser:
    return LabUser.objects.create(*args,**kwargs)

def filter_labuser(*args,**kwargs) -> QuerySet:
    return LabUser.objects.filter(*args,**kwargs)

def get_all_patientuser() -> QuerySet:
    return PatientUser.objects.all()

def create_patientuser(*args,**kwargs) -> PatientUser:
    return PatientUser.objects.create(*args,**kwargs)

def filter_patientuser(*args,**kwargs) -> QuerySet:
    return PatientUser.objects.filter(*args,**kwargs)