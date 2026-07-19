from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):

    default_owner_field = "user"

    def has_object_permission(self, request, view, obj):
        owner_field = getattr(view, "owner_field", self.default_owner_field)
        owner = getattr(obj, owner_field, None)
        return owner == request.user


class IsAdmin(BasePermission):

    message = "Bu amal faqat administratorlar uchun."

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )


class IsVerified(BasePermission):

    message = "Hisobingizni tasdiqlang (email yoki SMS orqali)."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "is_verified", False)
        )


class ReadOnlyOrIsAdmin(BasePermission):
    message = "Bu amalni faqat administrator bajara oladi."

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff