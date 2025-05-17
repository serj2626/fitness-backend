from django.core.exceptions import ValidationError
from PIL import Image


def validate_image_format(image):
    try:
        img = Image.open(image)
        if img.format not in ["JPEG", "PNG", "JPG", "WEBP"]:
            raise ValidationError("Допустимы только JPEG, PNG, JPG и WEBP форматы.")
    except Exception:
        raise ValidationError("Невозможно открыть изображение.")
