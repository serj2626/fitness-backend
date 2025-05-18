from django.contrib import admin

from common.mixins import AdminLimitMixin, AdminShortDescriptionMixin
from .models import Abonement, OrderAbonement, GymVisit


@admin.register(Abonement)
class AbonementAdmin(AdminShortDescriptionMixin, AdminLimitMixin, admin.ModelAdmin):
    """Admin View for Abonement"""
    singleton_limit = 3

    list_display = (
        "title",
        "get_description",
        "price",
        "number_of_months",
        "slug",
    )


@admin.register(OrderAbonement)
class OrderAbonementAdmin(AdminShortDescriptionMixin, admin.ModelAdmin):
    """Admin View for OrderAbonement"""

    list_display = (
        "user",
        "abonement",
        "start",
        "end",
        "status",
        "active",
    )


@admin.register(GymVisit)
class GymVisitAdmin(AdminShortDescriptionMixin, admin.ModelAdmin):
    """Admin View for GymVisit"""

    list_display = (
        "user",
        "visit_start",
        "visit_end",
        "total_time",
    )