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
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.reason

class PreventionLog(models.Model):
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.reason

class PromiscuoDirectory(models.Model):
    path = models.CharField(max_length=500)
    def __str__(self) -> str:
        return self.path
    
class QuarentineDirectory(models.Model):
    path = models.CharField(max_length=500)
    def __str__(self) -> str:
        return self.path
    
class SecureLogDirectory(models.Model):
    path = models.CharField(max_length=500)
    def __str__(self) -> str:
        return self.path
class MessageLogDirectory(models.Model):
    path = models.CharField(max_length=500)
    def __str__(self) -> str:
        return self.path
