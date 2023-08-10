from rest_framework import serializers
from .models import Bill,BillItem,Test
from accounts.serializers import PatientUserSerializer


class BillSerializers(serializers.ModelSerializer):
    patientuser = PatientUserSerializer()

    class Meta:
        model = Bill
        fields = '__all__'

class TestSerializers(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = '__all__'

    
class BillItemSerializers(serializers.ModelSerializer):

    test = TestSerializers()

    class Meta:
        model = BillItem
        fields = '__all__'

class UnnestedBillItemSerializers(serializers.ModelSerializer):

    class Meta:
        model = BillItem
        fields = '__all__'

class BillDetailedSerializers(serializers.ModelSerializer):
    bill_items = UnnestedBillItemSerializers(many=True,read_only=True)

    class Meta:
        model = Bill
        fields = '__all__'



