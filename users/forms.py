from django import forms
from django.contrib.auth import get_user_model

from team_finder.validators import normalize_phone, validate_github_url

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("name", "surname", "email", "password")
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "email": "Email",
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].strip().lower()
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("name", "surname", "avatar", "about", "phone", "github_url")
        labels = {
            "name": "Имя",
            "surname": "Фамилия",
            "avatar": "Аватар",
            "about": "О себе",
            "phone": "Телефон",
            "github_url": "GitHub",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Введите имя"}),
            "surname": forms.TextInput(attrs={"placeholder": "Введите фамилию"}),
            "about": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Коротко расскажите о себе"}
            ),
            "phone": forms.TextInput(attrs={"placeholder": "+79991234567"}),
            "github_url": forms.URLInput(
                attrs={"placeholder": "https://github.com/username"}
            ),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "")
        normalized_phone = normalize_phone(phone)
        if not normalized_phone:
            return ""

        qs = User.objects.filter(phone=normalized_phone)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Этот номер уже используется другим пользователем.")
        return normalized_phone

    def clean_github_url(self):
        github_url = self.cleaned_data.get("github_url", "").strip()
        return validate_github_url(github_url)
