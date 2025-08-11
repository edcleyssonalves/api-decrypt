from rest_framework import serializers
from .models import PaymentProof


class PaymentProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProof
        fields = [
            'id',
            'contact_name',
            'contact_number',
            'chat_id',
            'media_type',
            'media_key',
            'media_url',
            'file',
            'received_at',
            'processed_at',
            'status',
        ]

        read_only_fields = ['id', 'file', 'received_at', 'processed_at', 'status']
