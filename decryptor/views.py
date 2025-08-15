from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.core.files.base import ContentFile
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import PaymentProof
from .serializers import PaymentProofSerializer
from .utils import descriptografar_midia, ler_arquivo
import re



class PaymentProofCreateListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    queryset = PaymentProof.objects.all()
    serializer_class = PaymentProofSerializer


class PaymentProofReadFile(generics.RetrieveAPIView):
    """
    Lê o conteúdo do arquivo de um PaymentProof já salvo e retorna o texto completo
    e campos extraídos quando possível.
    """
    permission_classes = [IsAuthenticated]
    queryset = PaymentProof.objects.all()
    serializer_class = PaymentProofSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        proof = self.get_object()

        if not proof.file:
            raise ValidationError({"error": "Arquivo não encontrado."})

        try:
            # Lê bytes do arquivo via FileField
            with proof.file.open('rb') as f:
                conteudo_bytes = f.read()

            ext = proof.file.name.split(".")[-1]
            ext = f".{ext.lower()}"

            # Extrai texto (PDF ou imagem)
            texto = ler_arquivo(conteudo_bytes, ext)

            # Campos opcionais extraídos via regex
            valor_match = re.search(r"R\$ ?[\d.,]+", texto)
            data_match = re.search(r"\d{2} \w{3} \d{4}", texto)
            pix_match = re.search(r"\+?\d{10,15}", texto)  # captura número de celular ou chave Pix
            nome_match = re.search(r"Nome[:\s]+([A-Z\s]+)", texto, re.IGNORECASE)

            json_flexivel = {
                "id": proof.id,
                "texto_completo": texto,
                "campos_extraidos": {
                    "valor": valor_match.group(0) if valor_match else None,
                    "data": data_match.group(0) if data_match else None,
                    "pix": pix_match.group(0) if pix_match else None,
                    "nome_pagador": nome_match.group(1).strip() if nome_match else None
                }
            }

            return Response(json_flexivel)

        except Exception as e:
            raise ValidationError({"error": str(e)})


class PaymentProofReadAllFiles(generics.ListAPIView):
    """
    Retorna o texto completo e campos extraídos de todos os PaymentProofs processados.
    """
    permission_classes = [IsAuthenticated]
    queryset = PaymentProof.objects.filter(status="processed")  # apenas processados
    serializer_class = PaymentProofSerializer

    def list(self, request, *args, **kwargs):
        results = []

        for proof in self.get_queryset():
            if not proof.file:
                continue  # pula se não tiver arquivo

            try:
                with proof.file.open('rb') as f:
                    conteudo_bytes = f.read()

                ext = proof.file.name.split(".")[-1]
                ext = f".{ext.lower()}"

                texto = ler_arquivo(conteudo_bytes, ext)

                # Campos opcionais via regex
                valor_match = re.search(r"R\$ ?[\d.,]+", texto)
                data_match = re.search(r"\d{2} \w{3} \d{4}", texto)
                pix_match = re.search(r"\+?\d{10,15}", texto)
                nome_match = re.search(r"Nome[:\s]+([A-Z\s]+)", texto, re.IGNORECASE)

                results.append({
                    "id": proof.id,
                    "texto_completo": texto,
                    "campos_extraidos": {
                        "valor": valor_match.group(0) if valor_match else None,
                        "data": data_match.group(0) if data_match else None,
                        "pix": pix_match.group(0) if pix_match else None,
                        "nome_pagador": nome_match.group(1).strip() if nome_match else None
                    }
                })

            except Exception:
                continue  # ignora erros de leitura

        return Response(results)
