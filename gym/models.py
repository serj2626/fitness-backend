from django.db import models
from common.models import BaseID, BaseReview
from django.utils.text import slugify
from common.types import SERVICES_TYPE
from common.upload import compress_image
from common.upload_to import dynamic_upload_to
from common.validators import (
    validate_image_extension_and_format,
)


class Service(BaseID):
    """
    Услуга
    """

    type = models.CharField("Тип", max_length=100, choices=SERVICES_TYPE, default="gym")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    avatar = models.ImageField(
        "Фото",
        upload_to=dynamic_upload_to,
        blank=True,
        null=True,
        validators=[validate_image_extension_and_format],
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.type)
        if self.avatar:
            self.avatar = compress_image(self.avatar)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Услуга {self.get_type_display()}'


class GymReviews(BaseReview):
    """
    Отзывы о тренажерном зале
    """

    class Meta:
        verbose_name = "Отзыв о тренажерном зале"
        verbose_name_plural = "Отзывы о тренажерном зале"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отзыв от {self.user.email}" if self.user else "Anonymous"

    # @property
    # def time_age(self):
    #     return timesince(self.created_at)
