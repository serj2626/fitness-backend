from django.utils.html import format_html


class SingletonAdminInfoMixin:
    singleton_info_text = "Можно создать только один экземпляр"
    singleton_info_color = "red"
    singleton_limit = 1

    def get_desc(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            self.singleton_info_color,
            self.singleton_info_text,
        )

    get_desc.short_description = "Доп Инфа"

    def has_add_permission(self, request):
        return self.model.objects.count() < self.singleton_limit


class AdminLimitMixin:
    singleton_limit = 1

    def has_add_permission(self, request):
        return self.model.objects.count() < self.singleton_limit
