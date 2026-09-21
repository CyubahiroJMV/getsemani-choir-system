from django.contrib import admin
from .models import Member, Song, Contribution, Attendance

# Kurema no kuregisitira amashusho yose muri Django Admin Panel
admin.site.register(Member)
admin.site.register(Song)
admin.site.register(Contribution)
admin.site.register(Attendance)
