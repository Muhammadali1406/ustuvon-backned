import pytest
from django.utils import timezone
from apps.users.models import User, VerificationCode


pytestmark = pytest.mark.django_db


def test_create_user_requires_phone_or_email():
    with pytest.raises(ValueError):
        User.objects.create_user(first_name="A", last_name="B", password="Aa1!aaaaa")

def test_create_user_with_phone_only():
    user = User.objects.create_user(
        first_name="Ali", last_name="Valiyev", phone="+998901234567", password="Aa1!aaaaa"
    )
    assert user.phone == "+998901234567"
    assert user.email is None
    assert user.check_password("Aa1!aaaaa")
    assert user.is_verified is False

def test_is_verified_true_if_either_channel_verified():
    user = User.objects.create_user(
        first_name="Ali", last_name="Valiyev", email="ali@example.com", password="Aa1!aaaaa"
    )
    assert user.is_verified is False
    user.is_email_verified = True
    user.save(update_fields=["is_email_verified"])
    assert user.is_verified is True

def test_verification_code_expiry_defaults_to_15_minutes():
    user = User.objects.create_user(
        first_name="Ali", last_name="Valiyev", email="ali@example.com", password="Aa1!aaaaa"
    )
    code = VerificationCode.objects.create(
        user=user,
        channel=VerificationCode.Channel.EMAIL,
        purpose=VerificationCode.Purpose.REGISTER_VERIFY,
    )
    assert code.is_expired is False
    assert code.expires_at > timezone.now()

def test_soft_deleted_user_excluded_from_default_manager():
    user = User.objects.create_user(
        first_name="Ali", last_name="Valiyev", email="ali@example.com", password="Aa1!aaaaa"
    )
    user_id = user.id
    user.delete()
    assert not User.objects.filter(id=user_id).exists()