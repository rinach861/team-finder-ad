import hashlib
import io
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont

from .constants import (
    AVATAR_FONT_NAME,
    AVATAR_FONT_SIZE,
    AVATAR_HASH_BASE,
    AVATAR_IMAGE_FORMAT,
    AVATAR_IMAGE_MODE,
    AVATAR_IMAGE_SIZE,
    AVATAR_PALETTE,
    AVATAR_TEXT_ANCHOR,
    AVATAR_TEXT_COLOR,
    AVATAR_TEXT_POSITION,
    AVATAR_TEXTBOX_POSITION,
    DEFAULT_AVATAR_INITIAL,
    SKILL_NAME_MAX_LENGTH,
    USER_ABOUT_MAX_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_PHONE_MAX_LENGTH,
    USER_SURNAME_MAX_LENGTH,
)
from .managers import UserManager


def generate_avatar_with_initial(seed_text: str, initial: str) -> ContentFile:
    index = int(hashlib.md5(seed_text.encode("utf-8")).hexdigest(), AVATAR_HASH_BASE) % len(
        AVATAR_PALETTE
    )
    image = Image.new(AVATAR_IMAGE_MODE, AVATAR_IMAGE_SIZE, AVATAR_PALETTE[index])
    drawer = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(AVATAR_FONT_NAME, AVATAR_FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()

    try:
        drawer.text(
            AVATAR_TEXT_POSITION,
            initial,
            fill=AVATAR_TEXT_COLOR,
            font=font,
            anchor=AVATAR_TEXT_ANCHOR,
        )
    except TypeError:
        bbox = drawer.textbbox(AVATAR_TEXTBOX_POSITION, initial, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        drawer.text(
            (
                (AVATAR_IMAGE_SIZE[0] - text_width) / 2,
                (AVATAR_IMAGE_SIZE[1] - text_height) / 2,
            ),
            initial,
            fill=AVATAR_TEXT_COLOR,
            font=font,
        )

    buffer = io.BytesIO()
    image.save(buffer, format=AVATAR_IMAGE_FORMAT)
    return ContentFile(buffer.getvalue(), name=f"avatar_{uuid.uuid4().hex}.png")


class Skill(models.Model):
    name = models.CharField("Название", max_length=SKILL_NAME_MAX_LENGTH, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True)
    name = models.CharField("Имя", max_length=USER_NAME_MAX_LENGTH)
    surname = models.CharField("Фамилия", max_length=USER_SURNAME_MAX_LENGTH)
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True)
    phone = models.CharField("Телефон", max_length=USER_PHONE_MAX_LENGTH, blank=True, default="")
    github_url = models.URLField("GitHub", blank=True)
    about = models.CharField("О себе", max_length=USER_ABOUT_MAX_LENGTH, blank=True)
    skills = models.ManyToManyField(Skill, related_name="users", blank=True)
    is_active = models.BooleanField("Активен", default=True)
    is_staff = models.BooleanField("Админ", default=False)
    date_joined = models.DateTimeField("Дата регистрации", auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        ordering = ("-id",)
        verbose_name = "пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} {self.surname}".strip() or self.email

    def save(self, *args, **kwargs):
        if not self.avatar:
            first_char = (self.name[:1] or self.email[:1] or DEFAULT_AVATAR_INITIAL).upper()
            seed = f"{self.email}-{self.name}-{self.surname}"
            self.avatar = generate_avatar_with_initial(seed, first_char)
        super().save(*args, **kwargs)
