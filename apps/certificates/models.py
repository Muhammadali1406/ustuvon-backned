import uuid

from django.conf import settings
from django.db import models

from core.models import BaseModel


class CertificateStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    GENERATED = "generated", "Generated"
    FAILED = "failed", "Failed"


class Certificate(BaseModel):
    """
    A certificate generated based on the test result.
    One certificate for each successful test result.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="certificates",
    )
    result = models.OneToOneField(
        "result.UserTestResult",
        on_delete=models.CASCADE,
        related_name="certificate",
    )
    certificate_number = models.CharField(
        max_length=32,
        unique=True,
        editable=False,
        help_text="unique code used for public validation",
    )
    pdf_file = models.FileField(
        upload_to="certificates/%Y/%m/",
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=16,
        choices=CertificateStatus.choices,
        default=CertificateStatus.PENDING,
    )

    class Meta(BaseModel.Meta):
        indexes = BaseModel.Meta.indexes + [
            models.Index(fields=["certificate_number"]),
        ]
    
    def save(self, *args, **kwargs):
        if not self.certificate_number:
            self.certificate_number = self._generate_number()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_number():
        return f"UST-{uuid.uuid4().hex[:8].upper()}"

    def __str__(self):
        return self.certificate_number