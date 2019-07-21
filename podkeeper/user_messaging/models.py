from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Chat(models.Model):
	users = models.ManyToManyField(CustomUser)

class Message(models.Model):
	content = models.TextField(blank=True, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
	sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_by_user')
	chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True)
