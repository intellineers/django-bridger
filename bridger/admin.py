from django.contrib import admin

from .models import FrontendUserConfiguration
from .notifications.admin import NotificationModelAdmin


class FrontendUserConfigurationInline(admin.TabularInline):
    model = FrontendUserConfiguration
    extra = 0
    fields = ["id", "user", "config"]
    readonly_fields = ["id", "user", "config"]


@admin.register(FrontendUserConfiguration)
class FrontendUserConfigurationModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    fieldsets = (
        ("Main Information", {"fields": ("user", "parent_configuration", "config")}),
    )
    inlines = [FrontendUserConfigurationInline]
