from django.db import models

class AlarmLogDirectory(models.Model):
    path = models.CharField(max_length=500)
    def __str__(self) -> str:
        return self.path

class PrevetionLogDirectory(models.Model):
    path = models.CharField(max_length=500)
    def __str__(self) -> str:
        return self.path


class AlarmLog(models.Model):
    reason = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.reason

class PromiscuoDirectory(models.Model):
    path = models.CharField(max_length=500)
    def __str__(self) -> str:
        return self.path
    
