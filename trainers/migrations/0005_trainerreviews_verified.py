# Generated by Django 5.1 on 2025-05-17 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trainers", "0004_alter_trainer_phone"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainerreviews",
            name="verified",
            field=models.BooleanField(default=False, verbose_name="Проверен"),
        ),
    ]
