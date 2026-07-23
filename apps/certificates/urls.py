from django.urls import path

from .views import (
    CertificateDetailView,                 
    CertificateListView, 
    CertificateValidationView,
    
    )


app_name = "certificates"

urlpatterns = [
    path("", CertificateListView.as_view(), name="list"),
    path("<uuid:pk>/", CertificateDetailView.as_view(), name="detail"),
    path("validate/<str:certificate_number>/", CertificateValidationView.as_view(), name="validate")
]