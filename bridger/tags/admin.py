from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ("title", "color")
