from django.db import models
import uuid
from django_ckeditor_5.fields import CKEditor5Field


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