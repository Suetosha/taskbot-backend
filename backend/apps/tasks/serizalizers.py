from rest_framework import serializers

from .models import Task
from ..categories.models import Category


class TaskSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=Category.objects.all()
    )

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "due_at",
            "is_completed",
            "categories",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")
        if request and request.user and request.user.is_authenticated:
            self.fields["categories"].queryset = Category.objects.filter(user=request.user)
        else:
            self.fields["categories"].queryset = Category.objects.none()
