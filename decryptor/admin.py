from django.contrib import admin
from .models import PaymentProof
from django.utils.html import format_html


@admin.register(PaymentProof)
class PaymentProofAdmin(admin.ModelAdmin):
    list_display = ("contact_number", "media_type", "status", "received_at", "processed_at", "preview", "download_link")
    list_filter = ("status", "media_type", "received_at")
    search_fields = ("contact_number", "contact_name", "chat_id")
    readonly_fields = ("received_at", "processed_at")

    def preview(self, obj):
        if not obj.file:
            return "-"
        url = obj.file.url
        if obj.media_type == "document":
            # PDF preview usando iframe
            return format_html('<iframe src="{}" width="200" height="250"></iframe>', url)
        else:
            # Preview para imagens
            return format_html('<img src="{}" style="max-height: 100px;"/>', url)
    preview.short_description = "Preview"

    def download_link(self, obj):
        if not obj.file:
            return "-"
        url = obj.file.url
        return format_html('<a href="{}" download>Baixar</a>', url)
    download_link.short_description = "Download"
