from django.db import models
# from __future__ import unicode_literals
# Create your models here.

class cal(models.Model):
    client = models.CharField(max_length=10)
    score = models.FloatField(max_length=10)
    rank = models.FloatField(max_length=10)
