from django.db import models

from common.models import BaseDate
from common.types import CONTACTS_TYPE


class Contact(models.Model):
    """
    Модель контактов
    """

    type = models.CharField(
        max_length=50,
        choices=CONTACTS_TYPE,
        default="phone",
        verbose_name="Тип",
    )
    value = models.TextField(max_length=500, verbose_name="Значение")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"Контакт {self.get_type_display()}"


class Feedback(BaseDate):
    """
    Обратная связь
    """

    name = models.CharField("Имя", max_length=255)
    phone = models.CharField("Телефон", max_length=255)
    agree = models.BooleanField("Согласие", default=False)
    verified = models.BooleanField("Проверен", default=False)

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"

    def __str__(self):
        return self.title
