from rest_framework import serializers

from .models import *


class CurrentCamerasSerializer(serializers.ModelSerializer):

    class Meta:
        depth = 0
        model = Camera
        fields = ('uid', 'address', 'is_filled', 'last_img')


class AllCamerasSerializer(serializers.ModelSerializer):

    class Meta:
        depth = 0
        model = Camera
        fields = ('uid', 'x_coordinate', 'y_coordinate', 'is_filled')
