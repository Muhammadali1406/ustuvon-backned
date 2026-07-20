from core.serializers import BaseModelSerializer

from rest_framework import serializers

from .models import Certificate

class CertificateSerializer(BaseModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = [
            "id",
            "user",
            "result",
            "certificate_number",
            "pdf_file",
            "status",
            "created_at",
            "updated_at",
            "is_deleted",
            "deleted_at",
        ]
        read_only_fields = ['certificate_number', '']

        def get_user(self, obj):
            return {
                "id": obj.user.id,
                "username": obj.user.username,
            }