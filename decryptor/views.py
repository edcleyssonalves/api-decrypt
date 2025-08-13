from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.core.files.base import ContentFile
from rest_framework.exceptions import ValidationError

from .models import PaymentProof
from .serializers import PaymentProofSerializer
from .utils import descriptografar_midia
from core.permissions import GlobalDefaultPermission


class PaymentProofCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = PaymentProof.objects.all()
    serializer_class = PaymentProofSerializer

    def perform_create(self, serializer):
        proof = serializer.save(status="pending")

        try:
            conteudo, ext = descriptografar_midia(
                proof.media_url,
                proof.media_key,
                proof.media_type,
            )
            filename = f"proof_{proof.id}{ext}"
            proof.file.save(filename, ContentFile(conteudo), save=False)

            proof.status = "processed"
            proof.processed_at = timezone.now()
            proof.save()

        except Exception as e:
            proof.status = "error"
            proof.processed_at = timezone.now()
            proof.save()
            raise ValidationError({"error": str(e)})


class PaymentProofRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission)
    queryset = PaymentProof.objects.all()
    serializer_class = PaymentProofSerializer
