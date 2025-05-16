from django.db import models
import uuid
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timesince import timesince


class BaseID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseContent(models.Model):
    content = CKEditor5Field(blank=True, verbose_name="Описание", config_name="extends")

    class Meta:
        abstract = True


class BaseTitle(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")

    class Meta:
        abstract = True


class BaseDate(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True


class BaseReview(BaseID, BaseDate):
    name = models.CharField("Имя", max_length=100, null=True, blank=True)
    email = models.EmailField("Email", null=True, blank=True)
    rating = models.SmallIntegerField(
        "Рейтинг", default=5, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField("Текст отзыва", max_length=5000, null=True, blank=True)

    @property
    def time_age(self):
        return timesince(self.created_at)

    class Meta:
        abstract = True
