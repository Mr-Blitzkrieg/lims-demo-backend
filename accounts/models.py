from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.db import models
from commons.models import BaseModel
from django.utils import timezone
from rest_framework.authtoken.models import Token
from datetime import datetime

TIME_FOR_EXPIRATION_IN_MINUTES = 30

class CustomAccountManager(BaseUserManager):

    def create_superuser(self,email,password,**other_fields):
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True')
        
        return self.create_user(email,password,**other_fields)


    def create_user(self,email,password,contact_number=None,role='patient',**other_fields):
        if not email:
            raise ValueError('Email is not provided')
        email = self.normalize_email(email)
        user = self.model(email=email,contact_number=contact_number,role=role,**other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser,PermissionsMixin,BaseModel):

    role_choices = [('lab','Lab'),('patient','Patient')]

    email = models.EmailField(max_length=200,unique=True)
    contact_number = models.CharField(max_length=15,null=True,blank=True)
    role = models.CharField(max_length=12,choices=role_choices,default='patient')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def __str__(self):
        return str(self.email)
    
class ExpiringToken(Token):
    expiration = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expiration:
            self.expiration = timezone.now() + timezone.timedelta(minutes=TIME_FOR_EXPIRATION_IN_MINUTES)
        return super(ExpiringToken, self).save(*args, **kwargs)
    
class LabUser(BaseModel):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    department = models.CharField(max_length=100)
    address = models.CharField(max_length=120)
    city = models.CharField(max_length=70)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PatientUser(BaseModel):

    GENDER_CHOICES = [('male','Male'),
                      ('female','Female'),
                      ('others','Others')]

    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(max_length=12,choices=GENDER_CHOICES)
    height = models.IntegerField(null=True,default=0)
    weight = models.IntegerField(null=True,default=0)
    address = models.CharField(max_length=120,null=True,blank=True)
    city = models.CharField(max_length=70,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    pincode = models.CharField(max_length=10,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)

    def calculate_age(self):
        if self.date_of_birth:
            today = datetime.today()
            birthdate = self.date_of_birth
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            return age
        return None

    def __str__(self):
        return self.name


    
