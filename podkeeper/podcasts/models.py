from django.db import models
from accounts.models import Category, HostProfile

# Create your models here.

class Podcast(models.Model):
	title = models.CharField(max_length=256, blank=True, null=True)
	owner_email = models.EmailField(blank=True, null=True)
	cover_art_link = models.URLField(blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	itunes_id = models.CharField(max_length=20, blank=True, null=True)
	category = models.ManyToManyField(Category)
	host = models.ForeignKey(HostProfile, on_delete=models.CASCADE, blank=True, null=True, default=None)
	total_episodes = models.CharField(max_length=20, blank=True, null=True)
	first_episode_date = models.DateTimeField(null=True, blank=True)

class Episode(models.Model):
	title = models.CharField(max_length=256, blank=True, null=True)
	podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, blank=True, null=True, default=None)
	length = models.CharField(max_length=20, blank=True, null=True)
	description = models.TextField(blank=True, null=True)