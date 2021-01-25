from django.contrib import admin
from .models import Restaurant, Location, JobPosting, JobApplication
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Location)
admin.site.register(JobPosting)
admin.site.register(JobApplication)