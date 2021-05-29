from django.contrib import admin
from .models import HashFile, WhiteListUser

# Register your models here.

admin.site.register(HashFile)
admin.site.register(WhiteListUser)