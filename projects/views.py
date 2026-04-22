from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ProjectForm
from .models import Project
from .services import (
    get_project_with_related_or_404,
    get_projects_queryset,
    paginate_queryset,
)


def project_list_view(request):
    projects = get_projects_queryset().order_by("-created_at")
    page_obj = paginate_queryset(projects, request)
    context = {
        "projects": page_obj.object_list,
        "page_obj": page_obj,
    }
    return render(request, "projects/project_list.html", context)


def project_detail_view(request, project_id):
    project = get_project_with_related_or_404(project_id)
    return render(request, "projects/project-details.html", {"project": project})


@login_required
def create_project_view(request):
    form = ProjectForm(request.POST or None)
    if form.is_bound and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect("projects:detail", project_id=project.id)

    return render(request, "projects/create-project.html", {"form": form, "is_edit": False})


@login_required
def edit_project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.id:
        return HttpResponseForbidden("Редактировать проект может только автор.")

    form = ProjectForm(request.POST or None, instance=project)
    if form.is_bound and form.is_valid():
        form.save()
        return redirect("projects:detail", project_id=project.id)

    return render(request, "projects/create-project.html", {"form": form, "is_edit": True})


@login_required
@require_POST
def complete_project_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.owner_id != request.user.id or project.status != Project.STATUS_OPEN:
        return JsonResponse({"status": "error"}, status=HTTPStatus.FORBIDDEN)

    project.status = Project.STATUS_CLOSED
    project.save(update_fields=["status"])
    return JsonResponse({"status": "ok", "project_status": project.status})


@login_required
@require_POST
def toggle_participate_view(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if project.owner_id == request.user.id:
        return JsonResponse(
            {
                "status": "error",
                "detail": "Автор проекта уже считается участником.",
            },
            status=HTTPStatus.BAD_REQUEST,
        )

    is_participant = project.participants.filter(pk=request.user.pk).exists()
    if is_participant:
        project.participants.remove(request.user)
    else:
        project.participants.add(request.user)

    return JsonResponse({"status": "ok", "participant": not is_participant})


def root_redirect_view(request):
    return redirect("projects:list")
