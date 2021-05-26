from django.db import models

# Create your models here.

class HashFil(models.Model):
    """A model of a rock band."""
    hash = models.CharField(max_length=500)
    path_file = models.CharField(max_length=500, unique=True)

