from __future__ import annotations
from django.db.models import Q
from .models import User, VerificationCode


def get_user_by_identifier(identifier: str) -> User | None:
    return User.objects.filter(Q(phone=identifier) | Q(email=identifier)).first()

def get_valid_verification_code(user: User, *, purpose: str, code: str) -> VerificationCode | None:
    return (
        VerificationCode.objects.filter(user=user, purpose=purpose, code=code, is_used=False)
        .order_by("-created_at")
        .first()
    )