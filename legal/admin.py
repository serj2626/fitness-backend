from django.contrib import admin

from common.mixins import SingletonAdminInfoMixin
from .models import About, Offerta, Policy, CookiePolicy


@admin.register(About)
class AboutAdmin(SingletonAdminInfoMixin, admin.ModelAdmin):
    """
    Админка компании
    """

    list_display = ("title", "get_desc")


@admin.register(Offerta)
class OffertaAdmin(SingletonAdminInfoMixin, admin.ModelAdmin):
    """
    Админка оферты
    """

    list_display = ("title", "get_desc")


@admin.register(Policy)
class PolicyAdmin(SingletonAdminInfoMixin, admin.ModelAdmin):

    list_display = ("title", "get_desc")


@admin.register(CookiePolicy)
class CookiePolicyAdmin(SingletonAdminInfoMixin, admin.ModelAdmin):
    """
    Админка политики cookie
    """

    list_display = ("title", "get_desc")
