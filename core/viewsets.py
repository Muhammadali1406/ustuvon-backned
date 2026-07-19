from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class BaseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()