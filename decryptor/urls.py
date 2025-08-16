from django.urls import path
from .views import PaymentProofCreateListView, PaymentProofRetrieveUpdateDestroyView, PaymentProofReadFile, PaymentProofReadAllFiles


urlpatterns = [
    path('paymentproof/', PaymentProofCreateListView.as_view(), name='paymentproof-list-create'),
    path('paymentproof/<int:pk>/', PaymentProofRetrieveUpdateDestroyView.as_view(), name='paymentproof-detail'),
    path('paymentproof/<int:pk>/readfile/', PaymentProofReadFile.as_view(), name='paymentproof-readfile'),
    path('paymentproof/readfile/', PaymentProofReadAllFiles.as_view(), name='paymentproof-readfile')
]
