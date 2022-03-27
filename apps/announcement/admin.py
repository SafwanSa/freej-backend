from django.contrib import admin
from .models import *

admin.site.register(Announcement)
admin.site.register(BuildingAnnouncement)
admin.site.register(CampusAnnouncement)
admin.site.register(CommercialAnnouncement)
