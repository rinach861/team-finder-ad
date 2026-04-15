import json

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from .forms import LoginForm, ProfileForm, RegistrationForm
from .models import Skill

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")

    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users:login")

    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")

    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip().lower()
        password = form.cleaned_data["password"]
        user = authenticate(request, email=email, password=password)
        if user is None:
            form.add_error(None, "Неверный email или пароль.")
        else:
            login(request, user)
            return redirect("projects:list")

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("projects:list")


def user_detail_view(request, user_id):
    profile_user = get_object_or_404(
        User.objects.prefetch_related("skills", "owned_projects__participants"),
        pk=user_id,
    )
    return render(request, "users/user-details.html", {"user": profile_user})


@login_required
def edit_profile_view(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("users:detail", user_id=request.user.id)

    return render(request, "users/edit_profile.html", {"form": form, "user": request.user})


@login_required
def change_password_view(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)
        return redirect("users:detail", user_id=request.user.id)

    return render(request, "users/change_password.html", {"form": form})


def participants_list_view(request):
    participants = User.objects.prefetch_related("skills").order_by("-id")
    active_skill = request.GET.get("skill", "").strip()
    all_skills = Skill.objects.order_by("name")

    if active_skill:
        participants = participants.filter(skills__name__iexact=active_skill).distinct()

    paginator = Paginator(participants, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "participants": page_obj.object_list,
        "page_obj": page_obj,
        "all_skills": all_skills,
        "active_skill": active_skill,
    }
    return render(request, "users/participants.html", context)


@require_GET
def skills_autocomplete_view(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse([], safe=False)

    skills = Skill.objects.filter(name__istartswith=query).order_by("name").values("id", "name")[
        :10
    ]
    return JsonResponse(list(skills), safe=False)


def _json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except (TypeError, ValueError, UnicodeDecodeError):
        return {}


@login_required
@require_http_methods(["POST"])
def add_skill_view(request, user_id):
    if request.user.id != user_id:
        return HttpResponseForbidden("Недостаточно прав.")

    target_user = get_object_or_404(User, pk=user_id)
    payload = _json_body(request)
    skill_id = payload.get("skill_id")
    skill_name = " ".join(str(payload.get("name", "")).strip().split())

    created = False
    if skill_id:
        skill = get_object_or_404(Skill, pk=skill_id)
    elif skill_name:
        skill = Skill.objects.filter(name__iexact=skill_name).first()
        if skill is None:
            skill = Skill.objects.create(name=skill_name)
            created = True
    else:
        return JsonResponse({"status": "error", "detail": "Передайте skill_id или name."}, status=400)

    added = not target_user.skills.filter(pk=skill.pk).exists()
    if added:
        target_user.skills.add(skill)

    return JsonResponse(
        {
            "skill_id": skill.id,
            "id": skill.id,
            "name": skill.name,
            "created": created,
            "added": added,
        }
    )


@login_required
@require_POST
def remove_skill_view(request, user_id, skill_id):
    if request.user.id != user_id:
        return HttpResponseForbidden("Недостаточно прав.")

    target_user = get_object_or_404(User, pk=user_id)
    skill = get_object_or_404(Skill, pk=skill_id)
    removed = target_user.skills.filter(pk=skill.pk).exists()
    if removed:
        target_user.skills.remove(skill)

    return JsonResponse({"status": "ok", "removed": removed, "skill_id": skill.id})
