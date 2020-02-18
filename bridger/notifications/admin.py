from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationModelAdmin(admin.ModelAdmin):
    readonly_fields = ["timestamp_created"]
    autocomplete_fields = ["recipient"]
