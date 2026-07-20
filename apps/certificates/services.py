from .models import Certificate, CertificateStatus
from .selectors import get_user_certificates



def create_certificate_for_result(user, result):
    """
    Creates a certificate record for the test result (in PENDING state).
    The actual PDF generation is done via a separate Celery task (tasks.py).
    """
    certificate, _ = Certificate.objects.get_or_create(
        result=result,
        defaults={"user": user, "status": CertificateStatus.PENDING},
    )
    return certificate


def mark_certificate_generated(certificate: Certificate, pdf_file):
    certificate.pdf_file = pdf_file
    certificate.status = CertificateStatus.GENERATED
    certificate.save(update_fields=["pdf_file", "status", "updated_at"])
    return certificate


def mark_certificate_failed(certificate: Certificate):
    certificate.status = CertificateStatus.FAILED
    certificate.save(update_fields=["status", "updated_at"])
    return certificate