from django.db import models
from common.models import BaseID, BaseContent, BaseTitle
from django.utils.text import slugify


SERVICES_TYPE = [
    ("gym", "Безлимитные визиты"),
    ("unlimited_visits", "Безлимитные визиты"),
    ("pool", "Бассейн"),
    ("yoga", "Йога"),
    ("spa", "SPA"),
    ("cosmetology", "Косметология"),
    ("cycle", "Велотренажер"),
    ("water aerobics", "Водное аэробик"),
    ("dancing", "Танцы"),
]


class Service(BaseID, BaseTitle):
    """
    Услуга
    """

    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    avatar = models.ImageField("Фото", upload_to="services/", null=True, blank=True)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
