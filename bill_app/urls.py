from django.urls import path
from .views import (BillView,BillItemView,
                    TestView,IndividualBillView,
                    GetBillItemsView,GetBillReportForPatientView,
                    DownloadDocumentView,UpdateBillItems,GetBillData)


app_name="bill_app"

urlpatterns = [
    path('bill-view/',BillView.as_view(),name="bill-view"),
    path('bill-item/<int:bill_item_id>/',BillItemView.as_view(),name="bill-item-view"),
    path('individual-bill/<int:bill_id>/',IndividualBillView.as_view(),name="individual-bill"),
    path('test/',TestView.as_view(),name="test"),
    path('get-bill-items/<int:bill_id>/',GetBillItemsView.as_view(),name="get-bill-items"),
    path('get-patient-bills/',GetBillReportForPatientView.as_view(),name="get-patient-bills"),
    path('download-documents/<int:bill_id>/<str:doc_type>/',DownloadDocumentView.as_view(),name="download-receipt"),
    path('update-bill-items/<int:bill_id>/',UpdateBillItems.as_view(),name="update-bill-items"),
    path('get-detailed-bill/<int:bill_id>/',GetBillData.as_view(),name="get-detailed-bill"),
]