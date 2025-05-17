from django.contrib import admin
from .models import GymReviews, Service
from django.utils.html import mark_safe


@admin.register(GymReviews)
class GymReviewsAdmin(admin.ModelAdmin):
    """Admin View for GymReviews"""

    list_display = ("name", "email", "rating", "get_text", "verified")

    def get_text(self, obj):
        return f"{(str(obj.txt))[0:26]}..."

    get_text.short_description = "Текст"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("type", "slug", "get_image")

    def get_image(self, obj):
        if obj.avatar and hasattr(obj.avatar, "url"):
            return mark_safe(
                f'<img src="{obj.avatar.url}" style="border-radius: 50%;" width="70" height="70">'
            )
        return "Нет изображения"

    get_image.short_description = "Фото"
