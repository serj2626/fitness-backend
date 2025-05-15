from django.db import models
from django.utils import timezone
from abonements.models import OrderAbonement


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

    def refund(self):
        self.status = self.STATUS_REFUNDED
        self.save()