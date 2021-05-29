from django.db import models

# Create your models here.

class HashFile(models.Model):
    name = models.CharField(max_length=500)
    hash = models.CharField(max_length=500)
    path_file = models.CharField(max_length=500, unique=True)
    

    def __str__(self) -> str:
        return self.name

class WhiteListUser(models.Model):
    username =models.CharField(max_length=500,unique=True)
    def __str__(self) -> str:
        return self.username