from __future__ import annotations
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.exceptions import (
    ConflictServiceError,
    NotFoundServiceError,
    PermissionDeniedServiceError,
)
from . import selectors
from .models import User, VerificationCode
from .tasks import send_verification_code_task


def _issue_tokens(user: User) -> dict:
    refresh = RefreshToken.for_user(user)
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


def send_verification_request(user: User, *, channel: str, purpose: str) -> VerificationCode:
    code = VerificationCode.objects.create(user=user, channel=channel, purpose=purpose)
    send_verification_code_task.delay(str(user.id), code.code, channel, purpose)
    return code


def _confirm_verification_code(user: User, *, code: str, purpose: str) -> VerificationCode:
    verification = selectors.get_valid_verification_code(user, purpose=purpose, code=code)
    if verification is None:
        raise NotFoundServiceError("Kod noto'g'ri yoki topilmadi.")
    if verification.is_expired:
        raise ConflictServiceError("Kod muddati tugagan. Qaytadan so'rang.")
    verification.mark_used()
    return verification

def register_user(*, first_name, last_name, password, phone=None, email=None) -> dict:
    if not phone and not email:
        raise ConflictServiceError("Telefon raqam yoki email manzillaridan biri kiritilishi shart.")
    if phone and User.objects.filter(phone=phone).exists():
        raise ConflictServiceError("Bu telefon raqam allaqachon ro'yxatdan o'tgan.")
    if email and User.objects.filter(email=email).exists():
        raise ConflictServiceError("Bu email manzil allaqachon ro'yxatdan o'tgan.")

    user = User.objects.create_user(
        first_name=first_name,
        last_name=last_name,
        phone=phone or None,
        email=email or None,
        password=password,
    )

    channel = VerificationCode.Channel.SMS if phone else VerificationCode.Channel.EMAIL
    send_verification_request(user, channel=channel, purpose=VerificationCode.Purpose.REGISTER_VERIFY)

    return {"user": user, **_issue_tokens(user)}


def verify_registration(user: User, *, code: str) -> User:
    verification = _confirm_verification_code(
        user, code=code, purpose=VerificationCode.Purpose.REGISTER_VERIFY
    )
    if verification.channel == VerificationCode.Channel.SMS:
        user.is_phone_verified = True
        user.save(update_fields=["is_phone_verified"])
    else:
        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])
    return user


def login_user(*, identifier: str, password: str) -> dict:
    user = authenticate(identifier=identifier, password=password)
    if user is None:
        raise PermissionDeniedServiceError("Login yoki parol noto'g'ri.")
    return {"user": user, **_issue_tokens(user)}


def request_password_reset(*, identifier: str) -> None:
    user = selectors.get_user_by_identifier(identifier)
    if user is None:
        return

    channel = VerificationCode.Channel.SMS if user.phone == identifier else VerificationCode.Channel.EMAIL
    send_verification_request(user, channel=channel, purpose=VerificationCode.Purpose.PASSWORD_RESET)


def confirm_password_reset(*, identifier: str, code: str, new_password: str) -> None:
    user = selectors.get_user_by_identifier(identifier)
    if user is None:
        raise NotFoundServiceError("Foydalanuvchi topilmadi.")

    _confirm_verification_code(user, code=code, purpose=VerificationCode.Purpose.PASSWORD_RESET)
    user.set_password(new_password)
    user.save(update_fields=["password"])


def request_password_change(user: User) -> None:
    channel = VerificationCode.Channel.SMS if user.is_phone_verified else VerificationCode.Channel.EMAIL
    send_verification_request(user, channel=channel, purpose=VerificationCode.Purpose.PASSWORD_CHANGE)


def confirm_password_change(user: User, *, old_password: str, code: str, new_password: str) -> None:
    if not user.check_password(old_password):
        raise PermissionDeniedServiceError("Eski parol noto'g'ri.")

    _confirm_verification_code(user, code=code, purpose=VerificationCode.Purpose.PASSWORD_CHANGE)
    user.set_password(new_password)
    user.save(update_fields=["password"])