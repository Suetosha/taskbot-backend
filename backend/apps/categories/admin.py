from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("id", "name", "user__username", "user__email")
    ordering = ("name",)

    raw_id_fields = ("user",)

    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("name", "user")}),
        ("Служебные поля", {"fields": ("id", "created_at", "updated_at")}),
    )

    class Meta:
        unique_together = ("name", "user")
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
