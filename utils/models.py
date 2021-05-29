from django.db import models

class AlarmLogDirectory(models.Model):
    path = models.CharField(max_length=500)

class PrevetionLogAlarm(models.Model):
    path = models.CharField(max_length=500)

