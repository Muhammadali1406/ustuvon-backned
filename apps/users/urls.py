from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="auth-register"),
    path("login/", views.LoginView.as_view(), name="auth-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="auth-token-refresh"),
    path("verify/", views.VerifyRegistrationView.as_view(), name="auth-verify"),
    path("verify/resend/", views.ResendVerificationView.as_view(), name="auth-verify-resend"),
    path("password/reset/", views.PasswordResetRequestView.as_view(), name="auth-password-reset"),
    path(
        "password/reset/confirm/",
        views.PasswordResetConfirmView.as_view(),
        name="auth-password-reset-confirm",
    ),
    path("password/change/", views.PasswordChangeRequestView.as_view(), name="auth-password-change"),
    path(
        "password/change/confirm/",
        views.PasswordChangeConfirmView.as_view(),
        name="auth-password-change-confirm",
    ),
    path("me/", views.MeView.as_view(), name="auth-me"),
]