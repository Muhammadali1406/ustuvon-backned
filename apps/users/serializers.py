from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from core.serializers import BaseModelSerializer
from .models import User


class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "email",
            "is_phone_verified",
            "is_email_verified",
            "created_at",
            "updated_at",
        ]


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate(self, attrs):
        if not attrs.get("phone") and not attrs.get("email"):
            raise serializers.ValidationError(
                "Telefon raqam yoki email manzillaridan biri kiritilishi shart."
            )
        return attrs


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField(help_text="Telefon raqam yoki email")
    password = serializers.CharField(write_only=True)


class VerifyCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)


class PasswordResetRequestSerializer(serializers.Serializer):
    identifier = serializers.CharField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    code = serializers.CharField(max_length=6, min_length=6)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])


class PasswordChangeConfirmSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    code = serializers.CharField(max_length=6, min_length=6)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])


class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()