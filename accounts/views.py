from commons.views import BaseView
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from accounts.db_api import (get_customuser,create_customuser,get_or_create_token,
                             get_all_labuser,create_labuser,filter_labuser,
                             get_all_patientuser,create_patientuser,filter_patientuser)
from commons.api_response import api_error_response,api_success_response
from commons.db_utils import update_db_object
from rest_framework import permissions
from accounts.serializers import LabUserSerializer,PatientUserSerializer


class SignUpView(BaseView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        self.validate_field_in_params(request.data,['email','password'])
        email = request.data.get('email')
        user_data = {
            "email": email,
            "password": request.data.get('password'),
            "role": request.data.get('role','patient'),
            "contact_number": request.data.get('contact_number','')
        }

        try:
            get_customuser(email=email)
            return api_error_response(error_data={"error":"A user with this email already exits"})
        except ObjectDoesNotExist:
            user_instance = create_customuser(**user_data)

        if user_instance:
            token,_ = get_or_create_token(user=user_instance)

        return api_success_response(response_data={"message": "User created successfully","token": token.key},status=status.HTTP_201_CREATED)
    


class GetTokenView(BaseView):
    permission_classes = [permissions.AllowAny]

    def post(self,request):
        self.validate_field_in_params(request.data,['email','password'])
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user_instance = get_customuser(email=email)
        except ObjectDoesNotExist:
            return api_error_response(error_data={"error":"A user with this email does not exist"})
        
        if not user_instance.check_password(password):
            return api_error_response(error_data={"error":"Provided password is incorrect"})

        token,_ = get_or_create_token(user=user_instance)

        return api_success_response(response_data={"token": token.key})
    

class LabUserView(BaseView):

    def get(self,request):
        labusers_qs = get_all_labuser()
        serializer = LabUserSerializer(labusers_qs,many=True)
        return api_success_response(response_data={"labusers":serializer.data})
    
    def post(self,request):
        self.validate_field_in_params(request.data,['email','password','name','department','address',
                                                    'city','state','pincode','country'])
        
        user_data = {
            "email": request.data.get('email'),
            "password": request.data.get('password'),
            "role": 'lab',
            "contact_number": request.data.get('contact_number','')
        }
        try:
            get_customuser(email=user_data['email'])
            return api_error_response(error_data={"error":"A user with this email already exits"})
        except ObjectDoesNotExist:
            user_instance = create_customuser(**user_data)

        lab_user_data = {
            "user_id": user_instance.id,
            "name": request.data.get("name"),
            "department": request.data.get("department"),
            "address": request.data.get("address"),
            "city": request.data.get("city"),
            "state": request.data.get("state"),
            "pincode": request.data.get("pincode"),
            "country": request.data.get("country")
        }

        resp = {"message": "Lab User created successfully","token": ""}

        labuser_instance = create_labuser(**lab_user_data)
        if labuser_instance:
            token,_ = get_or_create_token(user=labuser_instance.user)
            resp.update({"token":token.key})

        return api_success_response(response_data=resp,status=status.HTTP_201_CREATED)
    

    
class IndividualLabUserView(BaseView):
     
     def patch(self,request,labuser_id):
        
        labuser_instance = filter_labuser(id=labuser_id).last()

        if not labuser_instance:
            return api_error_response(error_data={"error":"Lab User does not exist"}) 
        
        update_db_object(labuser_instance,request.data)

        return api_success_response(response_data={"message": "Lab User updated successfully"})
     

class PatientUserView(BaseView):

    def get(self,request):
        patientuser_qs = get_all_patientuser()
        serializer = PatientUserSerializer(patientuser_qs,many=True)
        return api_success_response(response_data={"patientusers":serializer.data})
    
    def post(self,request):
        self.validate_field_in_params(request.data,['email','password','name','gender']) 
        
        user_data = {
            "email": request.data.get('email'),
            "password": request.data.get('password'),
            "role": 'patient',
            "contact_number": request.data.get('contact_number','')
        }
        try:
            get_customuser(email=user_data['email'])
            return api_error_response(error_data={"error":"A user with this email already exits"})
        except ObjectDoesNotExist:
            user_instance = create_customuser(**user_data)

        patient_user_data = {
            "user_id": user_instance.id,
            "name": request.data.get("name"),
            "date_of_birth": request.data.get("date_of_birth",None),
            "gender": request.data.get("gender").lower(),
            "height": request.data.get("height",0),
            "weight": request.data.get("weight",0),
            "address": request.data.get("address"),
            "city": request.data.get("city"),
            "state": request.data.get("state"),
            "pincode": request.data.get("pincode"),
            "country": request.data.get("country")
        }

        resp = {"message": "Patient User created successfully","token": ""}

        patientuser_instance = create_patientuser(**patient_user_data)
        if patientuser_instance:
            token,_ = get_or_create_token(user=patientuser_instance.user)
            resp.update({"token":token.key})

        return api_success_response(response_data=resp,status=status.HTTP_201_CREATED)
    

    
class IndividualPatienUserView(BaseView):
     
    def get(self,request,patientuser_id):
        
        patientuser_instance = filter_patientuser(id=patientuser_id).last()

        if not patientuser_instance:
            return api_error_response(error_data={"error":"Patient User does not exist"}) 
        
        serializer = PatientUserSerializer(patientuser_instance)

        return api_success_response(response_data={**serializer.data})
     
    def patch(self,request,patientuser_id):
        
        patientuser_instance = filter_patientuser(id=patientuser_id).last()

        if not patientuser_instance:
            return api_error_response(error_data={"error":"Patient User does not exist"}) 
        
        update_db_object(patientuser_instance,request.data)

        return api_success_response(response_data={"message": "Patient User updated successfully"})

        

        

        









