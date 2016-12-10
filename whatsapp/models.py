from __future__ import unicode_literals

from django.db import models


class Conexe(models.Model):
    number = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
