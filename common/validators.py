import re
from django.core.exceptions import ValidationError
from PIL import Image
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


phone_regex = re.compile(r"^\+?7?\d{10}$")


phone_validator = RegexValidator(
    regex=phone_regex,
    message="Неправильный формат телефонного номера. Пример: +7 123 456 78 90 или 89123456789",
)


def validate_russian_phone(value):
    # Удаляем пробелы, дефисы, скобки
    cleaned = re.sub(r'[^\d+]', '', value)

    # Проверка на соответствие формату +7XXXXXXXXXX или 8XXXXXXXXXX
    if re.fullmatch(r'(\+7|8)\d{10}', cleaned) is None:
        raise ValidationError(
            _('Введите корректный российский номер телефона в формате +7XXXXXXXXXX или 8XXXXXXXXXX'),
            params={'value': value},
        )


def validate_image_extension_and_format(image):
    # 1. Проверка расширения (в нижнем регистре)
    valid_extensions = ["jpeg", "png", "jpg", "webp"]
    ext = image.name.split(".")[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            f"Недопустимое расширение файла: .{ext}. Разрешены: {', '.join(valid_extensions)}"
        )

    # 2. Проверка содержимого файла (формата изображения)
    try:
        img = Image.open(image)
        if (
            str(img.format).lower() not in valid_extensions
            and img.format not in valid_extensions
        ):
            raise ValidationError(
                f"Недопустимый формат изображения: {img.format}. Допустимы: JPEG, PNG."
            )
    except Exception:
        raise ValidationError(
            "Не удалось открыть изображение. Убедитесь, что файл — это допустимое изображение."
        )
