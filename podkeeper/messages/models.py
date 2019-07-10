from django.db import models
from podkeeper.accounts.models import CustomUser

# Create your models here.

class Message(models.Model):
	content = models.TextField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	recpient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)