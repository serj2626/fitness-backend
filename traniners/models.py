from django.db import models
from django.contrib.auth import get_user_model
from common.models import BaseContent, BaseID, BaseDate, BaseReview, BaseTitle
from common.types import POSITIONS_TYPE
from datetime import timedelta
from django.utils.timesince import timesince
from common.upload import compress_image
from common.upload_to import dynamic_upload_to
from common.validators import validate_image_extension_and_format, phone_validator, validate_russian_phone

User = get_user_model()


class Trainer(BaseID, BaseContent):
    """
    Тренер
    """

    position = models.CharField("Должность", max_length=100, choices=POSITIONS_TYPE)
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField(
        "Телефон", max_length=15, unique=True, validators=[validate_russian_phone]
    )
    avatar = models.ImageField(
        "Аватар",
        upload_to=dynamic_upload_to,
        blank=True,
        null=True,
        validators=[validate_image_extension_and_format],
    )

    class Meta:
        verbose_name = "Тренер"
        verbose_name_plural = "Тренеры"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_position_display()}"

    def save(self, *args, **kwargs):
        if self.avatar:
            self.avatar = compress_image(self.avatar)
        super().save(*args, **kwargs)


class TrainerImage(BaseID, BaseDate):
    """
    Фото тренера
    """

    trainer = models.ForeignKey(
        Trainer, on_delete=models.CASCADE, verbose_name="тренер", related_name="images"
    )
    image = models.ImageField(
        "Фото",
        upload_to=dynamic_upload_to,
        null=True,
        blank=True,
        validators=[validate_image_extension_and_format],
    )

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super().save(*args, **kwargs)

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

    @property
    def time_age(self):
        return timesince(self.created_at)

    class Meta:
        unique_together = (
            "trainer",
            "start",
            "end",
        )  # чтобы один тренер не был дважды на одно время
        verbose_name = "Забронированное занятие"
        verbose_name_plural = "Забронированные занятия"

    def __str__(self):
        return f"{self.trainer} — {self.start} - {self.end} ({'Занято' if self.is_booked else 'Свободно'})"


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
