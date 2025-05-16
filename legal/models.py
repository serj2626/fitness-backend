from django.db import models
from django.utils.text import slugify
from common.types import POST_CATEGORY_TYPES
from common.models import BaseContent, BaseID, BaseTitle, BaseDate


class Offerta(BaseTitle, BaseContent):
    """
    Оферта
    """

    class Meta:
        verbose_name = "Оферта"
        verbose_name_plural = "Оферта"

    def __str__(self):
        return f'Оферта "{self.title}"'


class Policy(BaseTitle, BaseContent):
    """
    Политика конфиденциальности
    """

    class Meta:
        verbose_name = "Политика конфиденциальности"
        verbose_name_plural = "Политика конфиденциальности"

    def __str__(self):
        return f"Политика конфиденциальности '{self.title}'"


class CookiePolicy(BaseTitle, BaseContent):
    """
    Политика cookie
    """

    class Meta:
        verbose_name = "Политика cookie"
        verbose_name_plural = "Политика cookie"

    def __str__(self):
        return f'Политика cookie "{self.title}"'

    class Meta:
        verbose_name = "Политика cookie"
        verbose_name_plural = "Политика cookie"


class About(BaseTitle, BaseContent):
    """
    О нас
    """

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"

    def __str__(self):
        return f'О нас "{self.title}"'

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"


class Post(BaseID, BaseTitle, BaseContent, BaseDate):
    """
    Модель поста
    """

    category = models.CharField(
        "Категория", max_length=100, choices=POST_CATEGORY_TYPES, default="hands"
    )
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
