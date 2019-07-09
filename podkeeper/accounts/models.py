from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.



class User(AbstractUser):
  PROFILE_CHOICES = (
      ('host', 'Host'),
      ('guest', 'Guest'),
  )
  active_profile = models.CharField(choices=PROFILE_CHOICES, default='host', max_length=6)


class GuestProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  signedup = models.BooleanField(default=False)
  rating = models.CharField(blank=True, default=None, max_length=6)


class HostProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  signedup = models.BooleanField(default=False)
  rating = models.CharField(blank=True, default=None, max_length=6)