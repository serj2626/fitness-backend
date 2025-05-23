# Generated by Django 5.1 on 2025-05-17 12:24

import common.upload_to
import common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gym", "0003_remove_service_title_alter_service_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="avatar",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=common.upload_to.dynamic_upload_to,
                validators=[common.validators.validate_image_extension_and_format],
                verbose_name="Фото",
            ),
        ),
    ]
