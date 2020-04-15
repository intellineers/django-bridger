from django.urls import path
from django.views.generic import TemplateView

from bridger.settings import bridger_settings


class FrontendView(TemplateView):
    template_name = bridger_settings.FRONTEND_TEMPLATE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["BRIDGER_CONTEXT"] = bridger_settings.FRONTEND_CONTEXT
        return context

    @classmethod
    def bundled_view(cls, url_path):
        return path(route=url_path, view=cls.as_view(), name="frontend")
