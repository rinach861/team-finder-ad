from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Skill, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("id",)
    list_display = ("id", "email", "name", "surname", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "name", "surname", "phone")
    readonly_fields = ("date_joined",)
    filter_horizontal = ("groups", "user_permissions", "skills")

    fieldsets = (
        ("Основное", {"fields": ("email", "password")}),
        ("Профиль", {"fields": ("name", "surname", "avatar", "about", "phone", "github_url")}),
        ("Навыки", {"fields": ("skills",)}),
        ("Права", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "surname", "password1", "password2"),
            },
        ),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
