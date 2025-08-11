from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from django.core.files.base import ContentFile

from .models import PaymentProof
from .serializers import PaymentProofSerializer
from .utils import descriptografar_midia

class PaymentProofCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PaymentProofSerializer(data=request.data)
        if serializer.is_valid():
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

                return Response(PaymentProofSerializer(proof).data, status=status.HTTP_201_CREATED)

            except Exception as e:
                proof.status = "error"
                proof.processed_at = timezone.now()
                proof.save()
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
