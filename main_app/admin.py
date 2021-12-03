from django.contrib.admin import AdminSite
from django.contrib import admin

from .models import *


class DogCameraAdmin(admin.ModelAdmin):
    list_display = ('address', 'uid', 'x_coordinate', 'y_coordinate', 'error_status', 'id', 'last_img', 'last_img_pred')


class DogCameraEventAdmin(admin.ModelAdmin):
    list_display = ('camera', 'dog_number')

class CameraAdmin(admin.ModelAdmin):
    list_display = ('address', 'uid', 'x_coordinate', 'y_coordinate', 'error_status', 'is_filled', 'id', 'last_img')


admin.site.register(UpdatedTime)
admin.site.register(Camera, CameraAdmin)
admin.site.register(CameraEvent)

admin.site.register(DogUpdatedTime)
admin.site.register(DogCamera, DogCameraAdmin)
admin.site.register(DogCameraEvent, DogCameraEventAdmin)
