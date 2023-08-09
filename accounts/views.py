from commons.views import BaseView
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from accounts.db_api import get_customuser,create_customuser,get_or_create_token
from commons.api_response import api_error_response,api_success_response
from rest_framework import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils import timezone
from datetime import timedelta


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






