from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    EmailField,
    ValidationError,
)
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()


class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True, min_length=8)
    password2 = CharField(write_only=True, min_length=8)
    email = EmailField(required=True)
    phone = CharField(required=True, max_length=20)

    class Meta:
        model = User
        fields = ("email", "phone", "password", "password2")

    def validate_email(self, value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise ValidationError("Введите корректный email адрес")

        if User.objects.filter(email=value).exists():
            raise ValidationError("Пользователь с таким email уже существует")

        return value.lower()  # Нормализуем email к нижнему регистру

    def validate_phone(self, value):
        # Удаляем все нецифровые символы для унификации
        cleaned_phone = re.sub(r"[^\d]", "", value)

        # Проверяем длину номера (для России обычно 11 цифр, включая код страны)
        if len(cleaned_phone) not in (10, 11):
            raise ValidationError("Номер телефона должен содержать 10 или 11 цифр")

        # Проверяем, что номер начинается правильно (для России)
        if not re.match(r"^[78]?\d{10}$", cleaned_phone):
            raise ValidationError("Введите корректный российский номер телефона")

        # Форматируем номер в единый формат (7XXXXXXXXXX)
        formatted_phone = f"+7{cleaned_phone[-10:]}"

        if User.objects.filter(phone=formatted_phone).exists():
            raise ValidationError("Пользователь с таким телефоном уже существует")

        return formatted_phone

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise ValidationError({"password2": "Пароли не совпадают"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            phone=validated_data["phone"],
            password=validated_data["password"],
        )
        return user
