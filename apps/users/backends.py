from django.contrib.auth.backends import ModelBackend
from .models import User


class PhoneOrEmailBackend(ModelBackend):
    def authenticate(self, request, identifier=None, password=None, **kwargs):
        if identifier is None or password is None:
            return None

        user = (
            User.objects.filter(phone=identifier).first()
            or User.objects.filter(email=identifier).first()
        )

        if user is None:
            User().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None