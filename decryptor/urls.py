from django.urls import path
from .views import PaymentProofCreateListView, PaymentProofRetrieveUpdateDestroyView

urlpatterns = [
    path('paymentproof/', PaymentProofCreateListView.as_view(), name='paymentproof-list-create'),
    path('paymentproof/<int:pk>/', PaymentProofRetrieveUpdateDestroyView.as_view(), name='paymentproof-detail')
]