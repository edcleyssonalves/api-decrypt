from django.contrib import admin
from django.utils.html import format_html
from .models import PaymentProof


@admin.register(PaymentProof)
class PaymentProofAdmin(admin.ModelAdmin):
    list_display = (
        "nome_contato",
        "numero_contato",
        "tipo_midia",
        "status",
        "recebido_em",
        "preview",
        "download_link",
    )

    list_filter = ("status", "media_type", "received_at")
    search_fields = ("contact_number", "contact_name", "chat_id")
    readonly_fields = ("received_at", "processed_at")

    def nome_contato(self, obj):
        return obj.contact_name
    nome_contato.short_description = "Nome do Contato"

    def numero_contato(self, obj):
        return obj.contact_number
    numero_contato.short_description = "WhatsApp"

    def tipo_midia(self, obj):
        return obj.media_type
    tipo_midia.short_description = "Tipo de Mídia"

    def recebido_em(self, obj):
        return obj.received_at
    recebido_em.short_description = "Data Recebimento"

    def preview(self, obj):
        if not obj.file:
            return "-"

        url = obj.file.url
        return format_html(
            '<a href="{}" target="_blank" class="button" style="padding:4px 10px; background:#1a73e8; color:#fff; border-radius:4px; text-decoration:none;">Visualizar</a>',
            url,
        )
    preview.short_description = "Preview"

    def download_link(self, obj):
        if not obj.file:
            return "-"
        url = obj.file.url
        return format_html(
            '<a href="{}" download style="font-weight:bold; color:#1a73e8;">Baixar</a>', url
        )
    download_link.short_description = "Download"
