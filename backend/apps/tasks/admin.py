from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "user",
        "due_at",
        "is_completed",
        "created_at",
        "updated_at",
    )
    list_filter = ("is_completed", "due_at", "created_at", "updated_at")
    search_fields = ("id", "title", "description", "user__username", "user__email")
    ordering = ("-created_at",)

    raw_id_fields = ("user",)
    filter_horizontal = ("categories",)

    date_hierarchy = "due_at"

    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("title", "description")}),
        ("Срок и статус", {"fields": ("due_at", "is_completed")}),
        ("Пользователь и категории", {"fields": ("user", "categories")}),
        ("Служебные поля", {"fields": ("id", "created_at", "updated_at")}),
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"