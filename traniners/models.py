from django.db import models
from django.contrib.auth import get_user_model
from common.models import BaseContent, BaseID, BaseDate, BaseReview, BaseTitle
from common.types import POSITIONS_TYPE
from datetime import timedelta


User = get_user_model()


class Trainer(BaseID, BaseContent):
    """
    Тренер
    """

    position = models.CharField("Должность", max_length=100, choices=POSITIONS_TYPE)
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Телефон", max_length=12, unique=True)
    avatar = models.ImageField(
        "Аватар",
        upload_to="trainers/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_position_display()}"


class TrainerImage(BaseID, BaseDate):
    """
    Фото тренера
    """

    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, verbose_name="тренер", related_name="images"
    )
    image = models.ImageField(
        "Фото",
        upload_to="trainers/images/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Фото {self.trainer}"

    class Meta:
        verbose_name = "Фото тренера"
        verbose_name_plural = "Фото тренеров"


class TrainerRate(BaseTitle):
    """
    Цены индивидульных тренировок
    """

    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, related_name="rates", verbose_name="тренер"
    )
    count_minutes = models.SmallIntegerField("Количество минут", blank=True, null=True)
    price = models.SmallIntegerField("Цена", default=1000)
    description = models.TextField("Описание тарифа", blank=True)

    class Meta:
        verbose_name = "Тариф тренера"
        verbose_name_plural = "Тарифы тренеров"
        ordering = ["-price"]

    def __str__(self):
        return (
            f"Индивидуальное занятие на {self.count_minutes} минут - тариф {self.title}"
        )


class TrainingSession(BaseID, BaseDate):
    """
    Забронировать занятие
    """

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trainings",
        verbose_name="Тренер",
    )
    client = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="trainings"
    )
    rate = models.ForeignKey(
        TrainerRate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="trainings",
        verbose_name="Тариф",
    )
    start = models.DateTimeField("Дата начала")
    end = models.DateTimeField("Конец", blank=True, null=True)
    is_booked = models.BooleanField(default=False, verbose_name="Занято")

    def save(self, *args, **kwargs):
        if not self.end:
            self.end = self.start + timedelta(self.rate.count_minutes)
        super().save(*args, **kwargs)

    class Meta:
        unique_together = (
            "trainer",
            "start",
            "end",
        )  # чтобы один тренер не был дважды на одно время

    # def __str__(self):
    #     return f"{self.trainer} — {self.date} {self.time} ({'Занято' if self.is_booked else 'Свободно'})"


class TrainerReviews(BaseReview):
    """
    Отзывы о тренерах
    """

    trainer = models.ForeignKey(
        Trainer,
        verbose_name="тренер",
        on_delete=models.CASCADE,
        related_name="trainer_reviews",
    )

    class Meta:
        verbose_name = "Отзыв о тренерах"
        verbose_name_plural = "Отзывы о тренерах"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отзыв от {self.user.email}" if self.user else "Anonymous"

    # @property
    # def time_age(self):
    #     return timesince(self.created_at)
