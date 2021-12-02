import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import random

from .models import *
from .serializers import *


class GetAllCamerasView(APIView):
    """
    Return all cameras data
    """

    @staticmethod
    def get(request):
        cameras = Camera.objects.all()
        cameras = AllCamerasSerializer(cameras, context={'request': request}, many=True).data
        return Response({
            'status': status.HTTP_200_OK,
            'data': {
                'timestamp': UpdatedTime.objects.all().first().value,
                'cameras': cameras
            }
        })


class GetCameraView(APIView):
    """
    Return camera data
    """

    @staticmethod
    def get(request, camera_uid):

        camera = Camera.objects.get(uid=camera_uid)
        camera = CurrentCamerasSerializer(camera, context={'request': request}).data
        camera['timestamp'] = UpdatedTime.objects.all().first().value
        return Response({
            'status': status.HTTP_200_OK,
            'data': {
                'camera': camera
            }
        })


class UpdateCamerasView(APIView):
    """
    Update and get cameras data
    """

    @staticmethod
    def get(request):
        cameras = Camera.objects.all()
        cameras = AllCamerasSerializer(cameras, context={'request': request}, many=True).data
        return Response({
            'status': status.HTTP_200_OK,
            'data': {
                'timestamp': UpdatedTime.objects.all().first().value,
                'cameras': cameras
            }
        })


class FillDatabaseView(APIView):
    """
    Fill database with test data
    """

    @staticmethod
    def get(request):
        list_of_errors = []

        try:
            if UpdatedTime.objects.all().exists():
                update_times = UpdatedTime.objects.all()
                update_times.delete()
            update_time = UpdatedTime()
            update_time.save()
        except Exception as e:
            list_of_errors.append(f"UpdatedTime adding: {str(e)}")

        try:
            if Camera.objects.all().exists():
                cameras = Camera.objects.all()
                cameras.delete()
            test_cameras = [
                {
                    'uid': 0,
                    'address': "Альметьевск; Белоглазова 131; ТКО"
                },
                {
                    'uid': 1,
                    'address': "Альметьевск; Белоглазова 151; ТКО"
                },
                {
                    'uid': 3,
                    'address': "Альметьевск; Гафиатуллина 29Б; ТКО"
                },
                {
                    'uid': 4,
                    'address': "Альметьевск; Гафиатуллина 39; ТКО"
                },
                {
                    'uid': 5,
                    'address': "Альметьевск; Гафиатуллина 45; ТКО"
                },
                {
                    'uid': 6,
                    'address': "Альметьевск; Гафиатуллина 47 (1): ТКО"
                },
                {
                    'uid': 7,
                    'address': "Альметьевск; Гафиатуллина 47 (2); ТКО"
                },
                {
                    'uid': 10,
                    'address': "Альметьевск; Ленина 66; ТКО"
                },
                {
                    'uid': 11,
                    'address': "Альметьевск; Ленина 90; ТКО"
                },
                {
                    'uid': 12,
                    'address': "Альметьевск; Шевченко 80; ТКО"
                },
                {
                    'uid': 14,
                    'address': "Альметьевск; Строителей 20Б; ТКО"
                },
                {
                    'uid': 15,
                    'address': "Альметьевск; Строителей 20; ТКО"
                },
            ]
            for el in test_cameras:
                camera = Camera(
                    uid=el['uid'],
                    address=el['address']
                )
                camera.save()
                camera.get_coordinates()

        except Exception as e:
            list_of_errors.append(f"UpdatedTime adding: {str(e)}")

        return Response({
            'status': status.HTTP_200_OK,
            'message': "Database filled with test data",
            'errors': list_of_errors
        })
