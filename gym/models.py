from django.db import models
from common.models import BaseID, BaseReview, BaseTitle
from django.utils.text import slugify
from common.types import SERVICES_TYPE


class Service(BaseID, BaseTitle):
    """
    Услуга
    """

    type = models.CharField("Тип", max_length=100, choices=SERVICES_TYPE, default="gym")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    avatar = models.ImageField("Фото", upload_to="services/", null=True, blank=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


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
