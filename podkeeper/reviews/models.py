from django.db import models
from accounts.models import CustomUser
# Create your models here.

class HostReview(models.Model):
  content = models.TextField(blank=True, null=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  reviewing_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="host_review_reviewer")
  reviewed_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="host_review_reviewee")


class GuestReview(models.Model):
  content = models.TextField(blank=True, null=True)
  timestamp = models.DateTimeField(auto_now_add=True)
  reviewing_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="guest_review_reviewer")
  reviewed_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="guest_review_reviewee")

