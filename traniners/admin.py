from django.contrib import admin

from common.mixins import ImagePreviewMixin
from .models import Trainer, TrainerImage, TrainerReviews, TrainingSession, TrainerRate
from django.utils.html import mark_safe


@admin.register(TrainerRate)
class TrainerRateAdmin(admin.ModelAdmin):
    """Admin View for Trainer)"""

    list_display = (
        "trainer",
        "count_minutes",
        "price",
        "description",
    )


@admin.register(TrainerReviews)
class TrainerReviewsAdmin(admin.ModelAdmin):
    """Admin View for TrainerReviews"""

    list_display = ("trainer", "name", "email", "rating", "get_text")

    def get_text(self, obj):
        return f"{(str(obj.txt))[0:26]}..."

    get_text.short_description = "Текст"


class TrainerImageInline(admin.TabularInline):
    model = TrainerImage
    extra = 1
    fields = ("image",)

    # def get_image(self, obj):
    #     if obj.image and hasattr(obj.image, "url"):
    #         return mark_safe(
    #             f'<img src="{obj.image.url}" style="border-radius: 50%;" width="50" height="50">'
    #         )
    #     return "Нет изображения"

    # get_image.short_description = "Фото"


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    """Admin View for Trainer)"""

    inlines = [TrainerImageInline]

    list_display = (
        "id",
        "position",
        "first_name",
        "last_name",
        "email",
        "phone",
        "get_avatar",
    )
    list_filter = ("position",)
    list_per_page = 5
    save_on_top = True
    search_fields = ("first_name", "last_name", "email", "phone")

    def get_avatar(self, obj):
        if obj.avatar and hasattr(obj.avatar, "url"):
            return mark_safe(
                f'<img src="{obj.avatar.url}" style="border-radius: 50%;" width="50" height="50">'
            )
        return "Нет изображения"

    get_avatar.short_description = "Фото"

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    """Admin View for TrainingSession"""

    list_display = (
        "trainer",
        "client",
        "rate",
        "start",
        "end",
        "is_booked",
    )
