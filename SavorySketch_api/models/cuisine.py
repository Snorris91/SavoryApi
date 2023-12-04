from django.db import models

class Cuisine(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)