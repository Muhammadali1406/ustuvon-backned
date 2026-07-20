from .models import Certificate

def get_certificate_by_number(certificate_number: str) -> Certificate | None:
    """
    Finds certificate by its number
    """
    return Certificate.objects.filter(
        certificate_number=certificate_number,
        status="generated",
    ).select_related("user", "result").first()


def get_user_certificates(user):
    """
    Returns user's certifications.
    """
    return Certificate.objects.filter(user=user).select_related("user", "result").order_by("-created_at")

