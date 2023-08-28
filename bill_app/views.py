from commons.views import BaseView
from django.core.exceptions import ObjectDoesNotExist
from bill_app.db_api import (create_bill,create_billitem,create_test,
                             get_test,get_billitem,get_all_bills,get_all_test,
                             get_bill,filter_bill)
from accounts.db_api import get_patientuser
from commons.api_response import api_success_response,api_error_response
from commons.db_utils import update_db_object
from rest_framework import status as http_status
from commons.permissions import AllowOnlyLabUsers,AllowOnlyPatientUsers
from bill_app.serializers import BillSerializers,TestSerializers,BillItemSerializers,BillDetailedSerializers
from django.template import loader
import pdfkit
from django.http import HttpResponse

class BillView(BaseView):
    permission_classes = [AllowOnlyLabUsers]

    def get(self,request):
        labusers_qs = get_all_bills()
        serializer = BillSerializers(labusers_qs,many=True)
        return api_success_response(response_data={"bills":serializer.data})

    def post(self,request):
        self.validate_field_in_params(request.data,['patientuser_id','bill_number','bill_items'])

        patientuser_id = request.data.get('patientuser_id')
        bill_number = request.data.get('bill_number')
        payment_status = request.data.get('payment_status','unpaid')
        bill_items = request.data.get('bill_items',[])

        try:
            patien_user_instance = get_patientuser(id=patientuser_id)
        except ObjectDoesNotExist:
            return api_error_response(error_data={"error": "Patient user does not exist" })
        
        bill_instance = create_bill(patientuser=patien_user_instance,bill_number=bill_number,
                                    payment_status=payment_status)
        total = 0

        for item in bill_items:
            test_id = item.get('test_id')
            value = item.get('value',0)
            quantity = item.get('quantity',1)
            status = item.get('status','pending')

            try:
                test_instance = get_test(id=test_id)
            except ObjectDoesNotExist:
                continue

            price = item.get('price') or test_instance.price
            
            sub_total = float(price) * int(quantity)
            total += sub_total

            create_billitem(bill=bill_instance,test=test_instance,
                            value=value,quantity=quantity,
                            price=price,sub_total=sub_total,status=status)
            
        
        update_db_object(bill_instance,{"total":total})

        bill_instance.update_bill_status_based_on_billitems()

        return api_success_response(response_data={
            "message": "Bill Created Successfully",
            "bill_id": bill_instance.id
        },status=http_status.HTTP_201_CREATED)
    
class IndividualBillView(BaseView):
    permission_classes = [AllowOnlyLabUsers]

    def patch(self,request,bill_id):
        try:
            bill_instance = get_bill(id=bill_id)
        except ObjectDoesNotExist:
            return api_error_response(error_data={"error":"Bill does not exist"})
        
        update_db_object(bill_instance,request.data)

        bill_instance.update_bill_status_based_on_billitems()

        return api_success_response(response_data={"message":"Bill updated successfully"})
    

class BillItemView(BaseView):

    permission_classes = [AllowOnlyLabUsers]

    def patch(self,request,bill_item_id):
        try:
            bill_item_instance = get_billitem(id=bill_item_id)
        except ObjectDoesNotExist:
            return api_error_response(error_data={"error":"Bill item does not exist"})
        
        update_db_object(bill_item_instance,request.data)

        bill_item_instance.bill.update_bill_status_based_on_billitems()

        return api_success_response(response_data={"message":"Bill Item updated successfully"})
    

class TestView(BaseView):

    permission_classes = [AllowOnlyLabUsers]

    def get(self,request):
        tests_qs = get_all_test()
        serializers = TestSerializers(tests_qs,many=True)
        return api_success_response(response_data={"tests":serializers.data})

    def post(self,request):
        self.validate_field_in_params(request.data,["name","unit"])
        name = request.data.get("name")
        test_data = {
            "name": name,
            "unit": request.data.get("unit"),
            "description": request.data.get("description",""),
            "reference_range": request.data.get("reference_range",""),
            "price": request.data.get("price",0.0)
        }
        try:
            get_test(name=name)
            return api_error_response(error_data={"error":"Test with this name already exist"})
        except ObjectDoesNotExist:
            create_test(**test_data)

        return api_success_response(response_data={"message":"Created Test successfully"})
    

class GetBillItemsView(BaseView):

    permission_classes = [AllowOnlyLabUsers]

    def get(self,request,bill_id):

        try:
            bill_instance = get_bill(id=bill_id)
        except ObjectDoesNotExist:
            return api_error_response(error_data={"error": "Bill does not exist"})
        
        bill_items_qs = bill_instance.billitem_set.all()

        serializer = BillItemSerializers(bill_items_qs,many=True)

        return api_success_response(response_data={"bill_items": serializer.data})
    

class GetBillView(BaseView):

    permission_classes = [AllowOnlyLabUsers]

    def get(self,request,bill_id):

        try:
            bill_instance = get_bill(id=bill_id)
        except ObjectDoesNotExist:
            return api_error_response(error_data={"error": "Bill does not exist"})
        
        bill_items_qs = bill_instance.billitem_set.all()

        serializer = BillItemSerializers(bill_items_qs,many=True)

        return api_success_response(response_data={"bill_items": serializer.data})

class GetBillReportForPatientView(BaseView):

    permission_classes = [AllowOnlyPatientUsers]

    def get(self,request):
        bills_qs = filter_bill(patientuser__user=request.user).prefetch_related('billitem_set')
        bills_data = []
        for bill in bills_qs:
            bill_serializer = BillSerializers(bill)
            bill_item_serializer = BillItemSerializers(bill.billitem_set.all(),many=True)
            bill_data = bill_serializer.data
            bill_data["bill_items"] = bill_item_serializer.data
            bills_data.append(bill_data)
        return api_success_response(response_data={"bills":bills_data})
    

            
class DownloadDocumentView(BaseView):
    
    def get(self, request, bill_id,doc_type):
        try:
            bill_instance = get_bill(id=bill_id)
        except ObjectDoesNotExist:
            return api_error_response(error_data={"error": "Bill does not exist"})
        
        if bill_instance.status != "completed":
            return api_error_response(error_data={"error": f"Report is {bill_instance.status}. Can't download !"})
        
        patient_age = bill_instance.patientuser.calculate_age()

        bill_items = bill_instance.billitem_set.all()

        DOC_NAME = 'receipt.html' if doc_type == 'RECEIPT' else 'report.html'
        
        template = loader.get_template(DOC_NAME)
        context = {
            'bill': bill_instance,
            'bill_items': bill_items,
            'patient_age': patient_age
        }
        html_content = template.render(context)
        
        pdf_file = pdfkit.from_string(html_content,False)
        
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=f"{DOC_NAME.lower()}.pdf"'
        
        return response
    
class UpdateBillItems(BaseView):
    permission_classes = [AllowOnlyLabUsers]

    def patch(self, request, bill_id):
        self.validate_field_in_params(request.data,["bill_items"])
        try:
            bill_instance = get_bill(id=bill_id)
        except ObjectDoesNotExist:
            return api_error_response(error_data={"error": "Bill does not exist"})
        
        bill_items_data = request.data["bill_items"]
        
        for item_data in bill_items_data:
            try:
                bill_item = get_billitem(id=item_data['id'], bill=bill_instance)
                update_db_object(bill_item,{"value":item_data["value"],"status":item_data["status"]})
            except ObjectDoesNotExist:
                pass

        bill_instance.update_bill_status_based_on_billitems()
        return api_success_response(response_data={"message":"Bill Items Updated Successfully"})
    

class GetBillData(BaseView):
    
    def get(self, request, bill_id):
        try:
            bill_instance = get_bill(id=bill_id)
        except ObjectDoesNotExist:
            return api_error_response(error_data={"error": "Bill does not exist"})

        bill_items = bill_instance.billitem_set.all()
        
        data = {
            'bill': BillSerializers(bill_instance).data,
            'bill_items': BillItemSerializers(bill_items,many=True).data,
        }
        return api_success_response(response_data={**data})
