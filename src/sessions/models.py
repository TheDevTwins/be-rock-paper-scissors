from django.db import models


class Session(models.Model):
    code = models.CharField(max_length=6, unique=True)
