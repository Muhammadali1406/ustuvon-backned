from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    HIDDEN_FIELDS = ("is_deleted", "deleted_at")
    READ_ONLY_FIELDS = ("created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.HIDDEN_FIELDS:
            self.fields.pop(field_name, None)

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        for field_name in self.READ_ONLY_FIELDS:
            extra_kwargs.setdefault(field_name, {})
            extra_kwargs[field_name]["read_only"] = True
        return extra_kwargs