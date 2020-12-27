from django.db import models


class User(models.Model):
    name = models.CharField(max_length=30, blank=True)
    surnames = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(blank=True)
    email = models.EmailField(blank=True, max_length=100)
    password = models.CharField(max_length=100, blank=True)
    verified = models.BooleanField(default=False)
    friends = models.ManyToManyField("User", blank=True)
    profile_pic = models.ImageField(null=True, blank=True)


class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE)
