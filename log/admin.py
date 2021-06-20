from django.contrib import admin
from log import models
# Register your models here.
admin.site.register(models.AlarmLog)
admin.site.register(models.PreventionLog)
