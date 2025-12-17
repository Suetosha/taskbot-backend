from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = DjangoUserAdmin.list_display + ("telegram_id", "id", "created_at", "updated_at")
    search_fields = DjangoUserAdmin.search_fields + ("telegram_id", "id")
    ordering = ("username",)

    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = DjangoUserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("telegram_id", "id", "created_at", "updated_at")}),
    )


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"