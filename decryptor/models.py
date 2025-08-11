from django.db import models

class PaymentProof(models.Model):
    # dados do contato
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=15)
    chat_id = models.CharField(max_length=255, blank=True, null=True)

    # dados da midia
    file = models.FileField(upload_to="proofs/", blank=True, null=True)
    media_type = models.CharField(max_length=20)  # ex: image, pdf
    media_key = models.TextField()
    media_url = models.URLField()

    # controle
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pendente"),
            ("processed", "Processado"),
            ("error", "Erro")
        ],
        default="pending"
    )
    
    def __str__(self):
        return f"{self.contact_number} - {self.media_type} - {self.status}"