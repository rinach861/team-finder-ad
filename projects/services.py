from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .constants import PROJECTS_PER_PAGE
from .models import Project


def get_projects_queryset():
    return Project.objects.select_related("owner").prefetch_related("participants")


def paginate_queryset(queryset, page_number, per_page=PROJECTS_PER_PAGE):
    paginator = Paginator(queryset, per_page)
    return paginator.get_page(page_number)


def get_project_with_related_or_404(project_id):
    return get_object_or_404(get_projects_queryset(), pk=project_id)
