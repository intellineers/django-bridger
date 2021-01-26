from django.contrib import admin

from .markdown.admin import AssetModelAdmin
from .models import FrontendUserConfiguration
from .notifications.admin import NotificationModelAdmin
from .tags.admin import TagModelAdmin
import csv
from django import forms
import pandas as pd
from django.http import HttpResponse
from django.urls import path
from django.shortcuts import render, redirect
from io import StringIO
import numpy as np

class FrontendUserConfigurationInline(admin.TabularInline):
    model = FrontendUserConfiguration
    extra = 0
    fields = ["id", "user", "config"]
    readonly_fields = ["id", "user", "config"]


@admin.register(FrontendUserConfiguration)
class FrontendUserConfigurationModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    fieldsets = (("Main Information", {"fields": ("user", "parent_configuration", "config")}),)
    inlines = [FrontendUserConfigurationInline]


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()

class ExportCsvMixin:
    def export_as_csv(self, admin, request, queryset, *args, **kwargs):
        meta = queryset.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions["export_as_csv"] = (self.export_as_csv, "export_as_csv", "Export Selected")
        return actions

class ImportCsvMixin:
    change_list_template = 'bridger/admin/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("import-csv/", self._import_csv)]
        return my_urls + urls

    def manipulate_df(self, df):
        return df
    
    def process_model(self, model):
        self.model.create(**model)
    
    def get_import_fields(self):
        return [f.name for f in self.model._meta.get_fields()]

    def _import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]

            str_text = ""
            for line in csv_file:
                str_text = str_text + line.decode()
            # Import csv as df
            df = pd.read_csv(StringIO(str_text))
            # Sanitize dataframe
            df = df.where(pd.notnull(df), None)
            df = df.drop(df.columns.difference(self.get_import_fields()), axis=1)

            # Overide this function if there is foreign key ids in the dataframe
            df = self.manipulate_df(df)
            errors = 0
            for model in df.to_dict("records"):
                #by default, process the modela as a create request. Can be override to change the behavior
                try:
                    self.process_model(model)
                except Exception as e:
                    errors += 1
                    pass
            self.message_user(request, f"Your csv file has been imported ( {df.shape[0] -errors }  imported, {errors} errors)")
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "bridger/admin/csv_form.html", payload)
