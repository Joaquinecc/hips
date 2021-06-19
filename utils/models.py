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
class HttpAccesLogDirectory(models.Model):
    path = models.CharField(max_length=500)
    def __str__(self) -> str:
        return self.path
class MailLogDirectory(models.Model):
    path = models.CharField(max_length=500)
    def __str__(self) -> str:
        return self.path
class MailQueueLimit(models.Model):
    qty=models.PositiveBigIntegerField()
    def __str__(self) -> str:
        return self.qty
class ProcessConsumeLimit(models.Model):
    max_cpu=models.PositiveBigIntegerField()
    max_ram=models.PositiveBigIntegerField()
    def __str__(self) -> str:
        return "max_cpu = "+self.max_cpu+" max_ram ="+self.max_ram
class ScriptType(models.Model):
    type=models.CharField(max_length=20)
    def __str__(self) -> str:
        return self.type
class Threshold(models.Model):
    threshold_fail_authentication_alarm=models.PositiveBigIntegerField()
    threshold_fail_authentication_prevention=models.PositiveBigIntegerField()