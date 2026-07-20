from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("certificate_number", "user", "status", "created_at")
    list_filter = ("status")
    search_fields = ("certificate_number", "user__username")
    readonly_fields = ("certificate_number", "created_at", "updated_at")
