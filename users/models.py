from django.db import models
import os
import base64
from django.conf import settings
import glob
import datetime


def get_custom_profile_path(instance, filename):
    # Purgue from past files or creates the folder containing the user profile image
    my_file_folder = base64.b64encode(
        bytes(instance.email, 'utf-8')).decode('utf-8')
    files = glob.glob(settings.MEDIA_ROOT + '/' + my_file_folder + '/*')
    for f in files:
        try:
            os.remove(f)
        except OSError:
            pass
    my_picture_path = '{0}/{1}'.format(my_file_folder, filename)
    return my_picture_path


class User(models.Model):
    name = models.CharField(max_length=30, blank=True)
    surnames = models.CharField(max_length=30, blank=True)
    birthday = models.DateField(blank=True)
    email = models.EmailField(blank=True, max_length=100)
    password = models.CharField(max_length=100, blank=True)
    verified = models.BooleanField(default=False)
    friends = models.ManyToManyField("User", blank=True)
    last_connection = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(
        null=True, blank=True, upload_to=get_custom_profile_path)


class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name='to_user', on_delete=models.CASCADE)
