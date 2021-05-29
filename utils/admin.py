from django.contrib import admin
from .models import AlarmLog,AlarmLogDirectory,PrevetionLogDirectory
# Register your models here.
admin.site.register(AlarmLog)
admin.site.register(AlarmLogDirectory)
admin.site.register(PrevetionLogDirectory)
