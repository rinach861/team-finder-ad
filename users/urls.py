from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("list/", views.participants_list_view, name="participants-list"),
    path("edit-profile/", views.edit_profile_view, name="edit-profile"),
    path("change-password/", views.change_password_view, name="change-password"),
    path("skills/", views.skills_autocomplete_view, name="skills-autocomplete"),
    path("<int:user_id>/skills/add/", views.add_skill_view, name="add-skill"),
    path(
        "<int:user_id>/skills/<int:skill_id>/remove/",
        views.remove_skill_view,
        name="remove-skill",
    ),
    path("<int:user_id>/", views.user_detail_view, name="detail"),
]
