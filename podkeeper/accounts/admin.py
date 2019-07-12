from django.contrib import admin
from .models import GuestProfile, HostProfile, Category
# Register your models here.

admin.site.register(GuestProfile)
admin.site.register(HostProfile)
admin.site.register(Category)