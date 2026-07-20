from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, VerificationCode


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ["-created_at"]
    list_display = ["phone", "email", "first_name", "last_name", "is_verified", "is_staff", "is_active"]
    list_filter = ["is_staff", "is_active", "is_phone_verified", "is_email_verified"]
    search_fields = ["phone", "email", "first_name", "last_name"]
    readonly_fields = ["id", "created_at", "updated_at", "last_login"]

    fieldsets = (
        (None, {"fields": ("phone", "email", "password")}),
        ("Shaxsiy ma'lumot", {"fields": ("first_name", "last_name")}),
        ("Tasdiqlash", {"fields": ("is_phone_verified", "is_email_verified")}),
        (
            "Ruxsatlar",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Muhim sanalar", {"fields": ("last_login", "created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone", "email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )

@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ["user", "channel", "purpose", "code", "is_used", "expires_at"]
    list_filter = ["channel", "purpose", "is_used"]
    search_fields = ["user__phone", "user__email", "code"]
    readonly_fields = ["code", "created_at"]