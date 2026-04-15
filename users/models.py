import hashlib
import io
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from .managers import UserManager


def generate_avatar_with_initial(seed_text: str, initial: str) -> ContentFile:
    palette = [
        "#3B82F6",
        "#16A34A",
        "#F59E0B",
        "#DB2777",
        "#0EA5E9",
        "#6366F1",
        "#DC2626",
        "#059669",
        "#7C3AED",
        "#0891B2",
    ]
    index = int(hashlib.md5(seed_text.encode("utf-8")).hexdigest(), 16) % len(palette)
    image = Image.new("RGB", (256, 256), palette[index])
    drawer = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except OSError:
        font = ImageFont.load_default()

    try:
        drawer.text((128, 128), initial, fill="white", font=font, anchor="mm")
    except TypeError:
        bbox = drawer.textbbox((0, 0), initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        drawer.text(
            ((256 - text_width) / 2, (256 - text_height) / 2),
            initial,
            fill="white",
            font=font,
        )

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=f"avatar_{uuid.uuid4().hex}.png")


class Skill(models.Model):
    name = models.CharField("Название", max_length=124, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True)
    name = models.CharField("Имя", max_length=124)
    surname = models.CharField("Фамилия", max_length=124)
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True)
    phone = models.CharField("Телефон", max_length=12, blank=True, default="")
    github_url = models.URLField("GitHub", blank=True)
    about = models.CharField("О себе", max_length=256, blank=True)
    skills = models.ManyToManyField(Skill, related_name="users", blank=True)
    is_active = models.BooleanField("Активен", default=True)
    is_staff = models.BooleanField("Админ", default=False)
    date_joined = models.DateTimeField("Дата регистрации", auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return f"{self.name} {self.surname}".strip() or self.email

    def save(self, *args, **kwargs):
        if not self.avatar:
            first_char = (self.name[:1] or self.email[:1] or "U").upper()
            seed = f"{self.email}-{self.name}-{self.surname}"
            self.avatar = generate_avatar_with_initial(seed, first_char)
        super().save(*args, **kwargs)
