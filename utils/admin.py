from django.contrib import admin
from utils import models
# Register your models here.
admin.site.register(models.AlarmLog)
admin.site.register(models.AlarmLogDirectory)
admin.site.register(models.PrevetionLogDirectory)
admin.site.register(models.PromiscuoDirectory)
admin.site.register(models.QuarentineDirectory)
admin.site.register(models.SecureLogDirectory)
admin.site.register(models.MessageLogDirectory)
admin.site.register(models.HttpAccesLogDirectory)



