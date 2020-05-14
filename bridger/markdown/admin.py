from django.contrib import admin

from .models import Asset


@admin.register(Asset)
class AssetModelAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "content_type")
    readonly_fields = ("content_type", "file_url_name")
