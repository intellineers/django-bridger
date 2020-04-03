from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import ModelTest, RelatedModelTest

admin.site.register(ModelTest, SimpleHistoryAdmin)
admin.site.register(RelatedModelTest, SimpleHistoryAdmin)
