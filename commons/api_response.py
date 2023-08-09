from rest_framework import status
from rest_framework.response import Response

def api_success_response(response_data:dict,status:int=status.HTTP_200_OK) -> Response:
    return Response(({"success":True,"data":response_data}),status=status)

def api_error_response(error_data:dict,status:int=status.HTTP_400_BAD_REQUEST) -> Response:
    return Response(({"success":True,"data":error_data}),status=status)