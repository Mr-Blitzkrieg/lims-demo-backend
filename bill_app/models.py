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
    STATUS_CHOICES = [('pending','Pending'),('partially completed','Partially Completed'),('completed','Completed')]

    patientuser = models.ForeignKey(PatientUser,on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=20)
    total = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    payment_status = models.CharField(max_length=10,choices=PAYMENT_STATUS_CHOICES,default='unpaid')
    status = models.CharField(max_length=30,choices=STATUS_CHOICES,default='pending')

    def update_bill_status_based_on_billitems(self):
        all_statuses = [item.status.lower() for item in self.billitem_set.all()]

        if all(status=='completed' for status in all_statuses):
            self.status = 'completed'
        elif any(status=='completed' for status in all_statuses):
            self.status = 'partially completed'
        else:
            self.status = 'pending'
        self.save()

    def __str__(self):
        return self.bill_number


class BillItem(BaseModel):

    STATUS_CHOICES = [('pending','Pending'),('completed','Completed')]

    bill = models.ForeignKey(Bill,on_delete=models.CASCADE)
    test = models.ForeignKey(Test,on_delete=models.SET_NULL,null=True)
    value = models.CharField(max_length=20,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    sub_total = models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return self.bill.id

