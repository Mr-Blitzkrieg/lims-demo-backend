from commons.models import BaseModel
from django.db import models
from accounts.models import PatientUser

class Test(BaseModel):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True,null=True)
    unit = models.CharField(max_length=20)
    reference_range=models.CharField(max_length=50,blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)

    def __str__(self):
        return self.name

class Bill(BaseModel):

    PAYMENT_STATUS_CHOICES = [('paid','Paid'),('unpaid','Unpaid')]

    patientuser = models.ForeignKey(PatientUser,on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    payment_status = models.CharField(max_length=10,choices=PAYMENT_STATUS_CHOICES,default='unpaid')

    def __str__(self):
        return self.bill_number


class BillItem(BaseModel):

    bill = models.ForeignKey(Bill,on_delete=models.CASCADE)
    test = models.ForeignKey(Test,on_delete=models.SET_NULL,null=True)
    value = models.CharField(max_length=20,blank=True,null=True)
    quantity = models.IntegerField(max_length=5,default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    sub_total = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)

    def __str__(self):
        return self.bill.id

