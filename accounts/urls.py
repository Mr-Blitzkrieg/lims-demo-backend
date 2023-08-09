from django.urls import path
from accounts.views import SignUpView,GetTokenView

app_name="accounts"

urlpatterns = [
    path('sign-up/',SignUpView.as_view(),name="sign-up-view"),
    path('get-token/',GetTokenView.as_view(),name="get-token")

]