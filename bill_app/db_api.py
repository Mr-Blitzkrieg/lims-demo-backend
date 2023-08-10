from bill_app.models import Test,Bill,BillItem
from django.db.models import QuerySet

def create_bill(*args,**kwargs) -> Bill:
    return Bill.objects.create(*args,**kwargs)

def get_all_bills() -> QuerySet:
    return Bill.objects.all()

def get_bill(*args,**kwargs) -> Bill:
    return Bill.objects.get(*args,**kwargs)

def filter_bill(*args,**kwargs) -> QuerySet:
    return Bill.objects.filter(*args,**kwargs)

def create_test(*args,**kwargs) -> Test:
    return Test.objects.create(*args,**kwargs)

def create_billitem(*args,**kwargs) -> BillItem:
    return BillItem.objects.create(*args,**kwargs)

def get_test(*args,**kwargs) -> Test:
    return Test.objects.get(*args,**kwargs)

def get_all_test() -> QuerySet:
    return Test.objects.all()

def get_billitem(*args,**kwargs) -> BillItem:
    return BillItem.objects.get(*args,**kwargs)