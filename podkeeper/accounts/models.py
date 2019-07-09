from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



class CustomUser(AbstractUser):
  PROFILE_CHOICES = (
      ('host', 'Host'),
      ('guest', 'Guest'),
  )
  active_profile = models.CharField(choices=PROFILE_CHOICES, default='host', max_length=6)


class GuestProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  signedup = models.BooleanField(default=False)
  rating = models.CharField(blank=True, default=None, max_length=6, null=True)


class HostProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  signedup = models.BooleanField(default=False)
  rating = models.CharField(blank=True, default=None, max_length=6, null=True)



@receiver(post_save, sender=CustomUser)
def create_profiles(sender, created, instance, **kwargs):
  if created:
    guest_profile = GuestProfile(user=instance)
    guest_profile.save()
    host_profile = HostProfile(user=instance)
    host_profile.save()