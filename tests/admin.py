from django.contrib import admin

from .models import ModelTest, RelatedModelTest

admin.site.register(ModelTest)
admin.site.register(RelatedModelTest)
