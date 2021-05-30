from django.contrib import admin
from task import models
# Register your models here.

admin.site.register(models.HashFile)
admin.site.register(models.WhiteListUser)
admin.site.register(models.BlackListApp)