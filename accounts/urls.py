from django.urls import path
from accounts.views import (SignUpView,GetTokenView,
                            LabUserView,IndividualLabUserView,
                            PatientUserView,IndividualPatienUserView)

app_name="accounts"

urlpatterns = [
    path('sign-up/',SignUpView.as_view(),name="sign-up-view"),
    path('get-token/',GetTokenView.as_view(),name="get-token"),
    path('lab-user/',LabUserView.as_view(),name="lab-user"),
    path('lab-user/<int:labuser_id>',IndividualLabUserView.as_view(),name="individual-lab-user"),
    path('patient-user/',PatientUserView.as_view(),name="patient-user"),
    path('patient-user/<int:patientuser_id>',IndividualPatienUserView.as_view(),name="individual-patient-user")

]