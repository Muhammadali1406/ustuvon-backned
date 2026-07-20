import random
import string
from datetime import timedelta
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from core.models import BaseModel


def generate_verification_code() -> str:
    return "".join(random.choices(string.digits, k=6))


class UserManager(BaseUserManager):


    use_in_migrations = True

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def _create_user(self, phone=None, email=None, password=None, **extra_fields):
        if not phone and not email:
            raise ValueError("Telefon raqam yoki email manzillaridan biri kiritilishi shart.")

        if email:
            email = self.normalize_email(email)

        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, email, password, **extra_fields)

    def create_superuser(self, phone=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_phone_verified", bool(phone))
        extra_fields.setdefault("is_email_verified", bool(email))
        extra_fields.setdefault("first_name", extra_fields.get("first_name", "Admin"))
        extra_fields.setdefault("last_name", extra_fields.get("last_name", "Admin"))

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser is_staff=True bo'lishi shart.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser is_superuser=True bo'lishi shart.")

        return self._create_user(phone, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return self.get_full_name() or self.phone or self.email or str(self.id)

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self) -> str:
        return self.first_name


    @property
    def is_verified(self) -> bool:
        return self.is_phone_verified or self.is_email_verified


class VerificationCode(BaseModel):

    class Channel(models.TextChoices):
        SMS = "sms", "SMS"
        EMAIL = "email", "Email"

    class Purpose(models.TextChoices):
        REGISTER_VERIFY = "register_verify", "Ro'yxatdan o'tishni tasdiqlash"
        PASSWORD_RESET = "password_reset", "Parolni tiklash"
        PASSWORD_CHANGE = "password_change", "Parolni o'zgartirishni tasdiqlash"


    DEFAULT_TTL_MINUTES = 15


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="verification_codes")
    channel = models.CharField(max_length=10, choices=Channel.choices)
    purpose = models.CharField(max_length=20, choices=Purpose.choices)
    code = models.CharField(max_length=6, default=generate_verification_code)
    expires_at = models.DateTimeField(blank=True)
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = "user_verification_codes"
        indexes = [models.Index(fields=["user", "purpose", "is_used"])]



    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=self.DEFAULT_TTL_MINUTES)
        super().save(*args, **kwargs)



    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at



    def mark_used(self):
        self.is_used = True
        self.save(update_fields=["is_used"])