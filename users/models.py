from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30, blank=True)
    surnames = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(blank=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=100, blank=True)
    verified = models.BooleanField(default=False)
