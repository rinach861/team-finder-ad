from django import forms

from team_finder.validators import validate_github_url

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "description", "github_url", "status")
        labels = {
            "name": "Название",
            "description": "Описание проекта",
            "github_url": "Ссылка на GitHub",
            "status": "Статус",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Введите название проекта"}),
            "description": forms.Textarea(
                attrs={"rows": 6, "placeholder": "Опишите идею проекта и кого ищете"}
            ),
            "github_url": forms.URLInput(
                attrs={"placeholder": "https://github.com/username/repository"}
            ),
            "status": forms.Select(),
        }

    def clean_github_url(self):
        github_url = self.cleaned_data.get("github_url", "").strip()
        return validate_github_url(github_url)
