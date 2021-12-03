from rest_framework import serializers

from .models import *


class CameraEventSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 0
        model = CameraEvent
        fields = ('id', 'containers_number', 'filled_containers_number')


class CurrentCamerasSerializer(serializers.ModelSerializer):
    # events = CameraEventAdmin(read_only=True, many=True)

    class Meta:
        depth = 0
        model = Camera
        fields = ('uid', 'address', 'is_filled', 'last_img')


class AllCamerasSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 0
        model = Camera
        fields = ('uid', 'x_coordinate', 'y_coordinate', 'is_filled')
