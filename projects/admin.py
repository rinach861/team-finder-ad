from django.contrib import admin
from django.db.models import Count

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "status", "participants_count", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "description", "owner__email", "owner__name", "owner__surname")
    autocomplete_fields = ("owner", "participants")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(_participants_count=Count("participants", distinct=True))

    @admin.display(description="Кол-во участников", ordering="_participants_count")
    def participants_count(self, obj):
        return obj._participants_count
