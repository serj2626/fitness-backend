from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from datetime import timedelta
import uuid
from django.utils import timezone

from django.forms import ValidationError


User = get_user_model()


class Abonement(models.Model):
    """Модель абонемента в фитнес-клуб"""

    TYPES = [
        # ("single", "Разовый визит"),
        # ("starter", "Начальный"),
        ("basic", "Базовый"),
        ("unlimited", "Безлимитный"),
        ("premium", "Премиум"),
    ]

    title = models.CharField("Название", max_length=100, choices=TYPES, default="basic")
    description = models.TextField("Описание")
    price = models.PositiveSmallIntegerField("Цена", null=True, blank=True)
    number_of_months = models.SmallIntegerField("Количество месяцев")

    class Meta:
        verbose_name = "Абонемент"
        verbose_name_plural = "Абонементы"
        ordering = ["price"]

    def __str__(self):
        return f"{self.get_name_display()} - {self.price}₽"


class OrderAbonement(models.Model):
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
    start = models.DateField("Начало", blank=True, null=True)
    end = models.DateField("Конец", blank=True, null=True)
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


class GymVisit(models.Model):
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


class Payment(models.Model):
    """
    Модель оплаты абонемента
    """

    # Статусы платежа
    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_REFUNDED = "refunded"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Ожидает оплаты"),
        (STATUS_COMPLETED, "Оплачен"),
        (STATUS_FAILED, "Ошибка оплаты"),
        (STATUS_REFUNDED, "Возврат"),
    ]

    # Способы оплаты
    METHOD_CARD = "card"
    METHOD_CASH = "cash"
    METHOD_TRANSFER = "transfer"

    METHOD_CHOICES = [
        (METHOD_CARD, "Карта"),
        (METHOD_CASH, "Наличные"),
        (METHOD_TRANSFER, "Перевод"),
    ]

    order = models.ForeignKey(
        OrderAbonement,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Заказ",
    )
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    status = models.CharField(
        "Статус", max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    payment_method = models.CharField(
        "Способ оплаты", max_length=20, choices=METHOD_CHOICES, default=METHOD_CARD
    )
    created_at = models.DateTimeField("Дата создания", default=timezone.now)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
    payment_date = models.DateTimeField("Дата оплаты", null=True, blank=True)
    transaction_id = models.CharField(
        "ID транзакции", max_length=100, null=True, blank=True
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Платеж #{self.id} - {self.amount} руб."

    def save(self, *args, **kwargs):
        # Если статус изменился на "оплачен", обновляем дату оплаты
        if self.status == self.STATUS_COMPLETED and not self.payment_date:
            self.payment_date = timezone.now()
            self.order.status = True  # Помечаем заказ как оплаченный
            self.order.active = True  # Активируем абонемент
            self.order.save()
        super().save(*args, **kwargs)
