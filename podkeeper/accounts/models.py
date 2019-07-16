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
  company_name = models.CharField(blank=True, default=None, max_length=20, null=True)
  website = models.URLField(blank=True, null=True)
  title = models.CharField(blank=True, default=None, max_length=80, null=True)
  email_confirmed = models.BooleanField(default=False)



class GuestProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  signedup = models.BooleanField(default=False)
  rating = models.CharField(blank=True, default=None, max_length=6, null=True)
  video_url = models.URLField(blank=True, null=True)
  desc = models.TextField(blank=True, null=True)


class HostProfile(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  signedup = models.BooleanField(default=False)
  rating = models.CharField(blank=True, default=None, max_length=6, null=True)
  ideal_guest_desc = models.TextField(blank=True, null=True)
  pub_email = models.EmailField(blank=True, null=True)


class Category(models.Model):
  value = models.CharField(blank=True, default=None, max_length=20, null=True)
  listen_note_id = models.IntegerField(blank=True, default=None, null=True)
  parent_listen_notes_id = models.IntegerField(blank=True, default=None, null=True)


class NotableGuest(models.Model):
  host = models.ForeignKey(HostProfile, on_delete=models.CASCADE)
  value = models.TextField(blank=True, null=True)


class Award(models.Model):
  guest = models.ForeignKey(GuestProfile, on_delete=models.CASCADE)
  value = models.TextField(blank=True, null=True)
  url = models.URLField(blank=True, null=True)


class Book(models.Model):
  guest = models.ForeignKey(GuestProfile, on_delete=models.CASCADE)
  value = models.TextField(blank=True, null=True)
  url = models.URLField(blank=True, null=True)

class TalkingPoint(models.Model):
  guest = models.ForeignKey(GuestProfile, on_delete=models.CASCADE)
  value = models.TextField(blank=True, null=True)

@receiver(post_save, sender=CustomUser)
def create_profiles(sender, created, instance, **kwargs):
  if created:
    guest_profile = GuestProfile(user=instance)
    guest_profile.save()
    host_profile = HostProfile(user=instance)
    host_profile.save()