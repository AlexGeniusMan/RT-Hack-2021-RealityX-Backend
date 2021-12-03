from django.contrib.admin import AdminSite
from django.contrib import admin

from .models import *


class CameraAdmin(admin.ModelAdmin):
    list_display = ('address', 'uid', 'x_coordinate', 'y_coordinate', 'error_status', 'is_filled', 'id', 'last_img')


admin.site.register(UpdatedTime)
admin.site.register(Camera, CameraAdmin)
admin.site.register(CameraEvent)
