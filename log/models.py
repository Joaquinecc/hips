from django.db import models

# Create your models here.

class AlarmLog(models.Model):
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.reason
class PreventionLog(models.Model):
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.reason