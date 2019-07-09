from django.contrib import admin
from .models import GuestProfile, HostProfile
# Register your models here.

admin.site.register(GuestProfile)
admin.site.register(HostProfile)