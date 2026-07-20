from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import services
from .models import VerificationCode
from .serializers import (
    LoginSerializer,
    PasswordChangeConfirmSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserSerializer,
    VerifyCodeSerializer,
)


def _auth_payload(result: dict) -> dict:
    return {
        "user": UserSerializer(result["user"]).data,
        "access": result["access"],
        "refresh": result["refresh"],
    }


class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = services.register_user(**serializer.validated_data)
        return Response(_auth_payload(result), status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = services.login_user(**serializer.validated_data)
        return Response(_auth_payload(result))


class VerifyRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.verify_registration(request.user, code=serializer.validated_data["code"])
        return Response({"detail": "Hisobingiz tasdiqlandi."})


class ResendVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        channel = VerificationCode.Channel.SMS if request.user.phone else VerificationCode.Channel.EMAIL
        services.send_verification_request(
            request.user, channel=channel, purpose=VerificationCode.Purpose.REGISTER_VERIFY
        )
        return Response({"detail": "Tasdiqlash kodi qayta yuborildi."})


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.request_password_reset(**serializer.validated_data)
        return Response({"detail": "Agar hisob mavjud bo'lsa, kod yuborildi."})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.confirm_password_reset(**serializer.validated_data)
        return Response({"detail": "Parol muvaffaqiyatli yangilandi."})


class PasswordChangeRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        services.request_password_change(request.user)
        return Response({"detail": "Tasdiqlash kodi yuborildi."})


class PasswordChangeConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.confirm_password_change(request.user, **serializer.validated_data)
        return Response({"detail": "Parol muvaffaqiyatli o'zgartirildi."})


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)