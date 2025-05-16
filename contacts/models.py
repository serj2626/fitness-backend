from django.db import models

TYPES_CONTACT = [
    # ТИПЫ КОНТАКТОВ
    ("phone", "Телефон"),
    ("mail", "Почта"),
    ("vk", "Вконтакте"),
    ("tg", "Телеграм"),
    ("whatsapp", "Ватсап"),
    ("address", "Адрес"),
    ("mode", "Режим работы"),
    ("latitude", "Широта"),
    ("longitude", "Долгота"),
]


class Contact(models.Model):
    """
    Модель контактов
    """

    type = models.CharField(
        max_length=50,
        choices=TYPES_CONTACT,
        default="phone",
        verbose_name="Тип",
    )
    value = models.TextField(max_length=500, verbose_name="Значение")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"Контакт {self.get_type_display()}"


class Feedback(models.Model):
    """
    Обратная связь
    """

    name = models.CharField("Имя", max_length=255)
    phone = models.CharField("Телефон", max_length=255)
    agree = models.BooleanField("Согласие", default=False)

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратная связь"

    def __str__(self):
        return self.title
