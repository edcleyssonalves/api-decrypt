from django.urls import path
from .views import PaymentProofCreateView

urlpatterns = [
    path('paymentproof/', PaymentProofCreateView.as_view(), name='paymentproof-create'),
]