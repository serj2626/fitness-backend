from django.db import models
from django.contrib.auth import get_user_model
from datetime import timedelta
from common.models import BaseID, BaseDate
from django.utils.text import slugify
from django.forms import ValidationError

from common.types import ABONEMENT_TYPES


User = get_user_model()


class Abonement(models.Model):
    """Модель абонемента в фитнес-клуб"""

    title = models.CharField(
        "Название", max_length=100, choices=ABONEMENT_TYPES, default="basic"
    )
    description = models.TextField("Описание")
    price = models.PositiveSmallIntegerField("Цена", null=True, blank=True)
    number_of_months = models.SmallIntegerField("Количество месяцев")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонементы"
        ordering = ["price"]

    def __str__(self):
        return f"{self.get_name_display()} - {self.price}₽"


class OrderAbonement(BaseID, BaseDate):
    """
    Забронировать абонемент
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="abonements", verbose_name="Клиент"
    )
    abonement = models.ForeignKey(
        Abonement,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Абонемент",
    )
    start = models.DateField("Начало абонемента")
    end = models.DateField("Конец абонемента", blank=True, null=True)
    status = models.BooleanField("Оплачен", default=False)
    active = models.BooleanField("Активен", default=False)

    def save(self, *args, **kwargs):
        if not self.end:
            count_days = self.abonement.number_of_months * 30
            self.end = self.start + timedelta(days=count_days)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Забронированный абонемент"
        verbose_name_plural = "Забронированные абонементы"

    def __str__(self):
        return f"Order - {self.abonement} - {self.user.email}"


class GymVisit(BaseDate):
    """
    Модель визита в фитнес-клуб
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="gym_visits",
        verbose_name="Пользователь",
    )
    order_abonement = models.ForeignKey(
        OrderAbonement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Абонемент",
        related_name="visits",
    )
    visit_start = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время начала визита",
    )
    visit_end = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True,
        verbose_name="Дата и время окончания визита",
    )

    class Meta:
        verbose_name = "Визит в фитнес-клуб"
        verbose_name_plural = "Визиты в фитнес-клуб"
        ordering = ["-visit_start"]

    def __str__(self):
        return f"{self.user.email} - {self.visit_start}"

    @property
    def total_time(self):
        """Возвращает продолжительность визита, если он завершен"""
        if not self.visit_end:
            return None
        return self.visit_end - self.visit_start

    def clean(self):
        """Проверка, что visit_end не раньше visit_start"""
        if self.visit_end and self.visit_end < self.visit_start:
            raise ValidationError("Дата окончания не может быть раньше даты начала!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
