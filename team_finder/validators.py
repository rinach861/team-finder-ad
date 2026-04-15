import re
from urllib.parse import urlparse

from django.core.exceptions import ValidationError

PHONE_PATTERN = re.compile(r"^(\+7|8)\d{10}$")


def normalize_phone(raw_phone: str) -> str:
    if not raw_phone:
        return ""

    compact_phone = re.sub(r"[^\d+]", "", raw_phone.strip())
    if not PHONE_PATTERN.match(compact_phone):
        raise ValidationError(
            "Телефон должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
        )

    if compact_phone.startswith("8"):
        compact_phone = f"+7{compact_phone[1:]}"
    return compact_phone


def validate_github_url(raw_url: str) -> str:
    if not raw_url:
        return ""

    parsed_url = urlparse(raw_url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        raise ValidationError("Укажите корректную ссылку.")

    netloc = parsed_url.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]

    if netloc != "github.com":
        raise ValidationError("Ссылка должна вести на github.com.")

    return raw_url
