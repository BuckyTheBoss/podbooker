from django.db import models
from podkeeper.accounts.models import Category, HostProfile

# Create your models here.

class Podcast(models.Model):
	title = models.CharField(max_length=256, blank=True, null=True)
	owner_email = models.EmailField(blank=True, null=True)
	cover_art_link = models.URLField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	itunes_url = models.URLField(blank=True, null=True)
	category = models.ManyToManyField(Category)
	host = models.ForeginKey(HostProfile, on_delete=models.CASCADE, blank=True, null=True, default=None)

class Episode(models.Model):
	title = models.CharField(max_length=256, blank=True, null=True)
	podcast = models.ForeginKey(Podcast, on_delete=models.CASCADE, blank=True, null=True, default=None)
	number = models.CharField(max_length=20, blank=True, null=True)
	description = models.TextField(blank=True, null=True)