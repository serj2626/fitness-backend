from django.core.exceptions import ValidationError
from PIL import Image


# def validate_image_format(image):
#     try:
#         img = Image.open(image)
#         if img.format not in ["JPEG", "PNG", "JPG", "WEBP"]:
#             raise ValidationError("Допустимы только JPEG, PNG, JPG и WEBP форматы.")
#     except Exception:
#         raise ValidationError("Невозможно открыть изображение.")


def validate_image_extension_and_format(image):
    # 1. Проверка расширения (в нижнем регистре)
    valid_extensions = ["JPEG", "PNG", "JPG", "WEBP"]
    ext = image.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Недопустимое расширение файла: .{ext}. Разрешены: {', '.join(valid_extensions)}")

    # 2. Проверка содержимого файла (формата изображения)
    try:
        img = Image.open(image)
        if img.format not in valid_extensions:
            raise ValidationError(f"Недопустимый формат изображения: {img.format}. Допустимы: JPEG, PNG.")
    except Exception:
        raise ValidationError("Не удалось открыть изображение. Убедитесь, что файл — это допустимое изображение.")