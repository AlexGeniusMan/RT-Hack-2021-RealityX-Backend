from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

import random
import boto3
from botocore import UNSIGNED
from botocore.client import Config

from .models import *
from .serializers import *

if (ML_ADDRESS := os.getenv("BACKEND_ML_ADDRESS")) is None:
    print("'BACKEND_ML_ADDRESS' env variable is not defined")
    sys.exit()


class GetAllDogCamerasView(APIView):
    """
    Return all cameras data
    """

    @staticmethod
    def get(request):
        cameras = DogCamera.objects.all()
        cameras = AllDogCamerasSerializer(cameras, context={'request': request}, many=True).data

        for camera in cameras:
            camera_events = DogCameraEvent.objects.filter(camera__uid=camera['uid']).order_by('-id')[0:30]
            number_of_dogs = 0
            for event in camera_events:
                number_of_dogs += event.dog_number
            camera['number_of_dogs'] = number_of_dogs

        return Response({
            'status': status.HTTP_200_OK,
            'data': {
                'timestamp': DogUpdatedTime.objects.all().first().value,
                'cameras': cameras
            }
        })


class UpdateDogCamerasView(APIView):
    """
    Update and get cameras data
    """

    @staticmethod
    def get(request):
        session = boto3.session.Session()

        s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            config=Config(signature_version=UNSIGNED)
        )

        cameras = DogCamera.objects.all()
        for camera in cameras:
            probability_of_dogs = random.randrange(1, 11)
            if probability_of_dogs < 3:
                print('True')
                source = 'dogs_clear'
            else:
                print('False')
                source = 'dogs'
            images = []
            for key in s3.list_objects(Bucket='reality-x', Prefix=f'{source}/{camera.uid}/')['Contents']:
                if not key['Key'].lower().endswith('/'):
                    images.append(f'https://s3.yandexcloud.net/reality-x/{key["Key"]}')
            while True:
                new_last_img_name = images[random.randrange(len(images))]
                if not camera.last_img == new_last_img_name:
                    camera.last_img = new_last_img_name
                    break
            camera.save()

        cameras = DogCamera.objects.all()

        data = {
            "img_size": 640,
            "conf": 0.3,
            "urls": [
                camera.last_img for camera in cameras
            ]
        }

        response = requests.post(f'{ML_ADDRESS}dogs/', timeout=10000,
                                 json=data).json()
        print(response)
        for el in response:
            camera_uid = el['url'].split('/')[-2]
            camera = DogCamera.objects.get(uid=camera_uid)
            camera.last_img_pred = el['url']
            camera.save()

            camera_event = DogCameraEvent(
                dog_number=el['n_all'],
                camera=camera
            )
            camera_event.save()

        update_time = DogUpdatedTime.objects.all().first()
        update_time.set_new_time()

        cameras = DogCamera.objects.all()
        cameras = AllDogCamerasSerializer(cameras, context={'request': request}, many=True).data

        for camera in cameras:
            camera_events = DogCameraEvent.objects.filter(camera__uid=camera['uid']).order_by('-id')[0:30]
            number_of_dogs = 0
            for event in camera_events:
                number_of_dogs += event.dog_number
            camera['number_of_dogs'] = number_of_dogs

        return Response({
            'status': status.HTTP_200_OK,
            'data': {
                'timestamp': DogUpdatedTime.objects.all().first().value,
                'cameras': cameras
            }
        })


class GetDogCameraView(APIView):
    """
    Return camera data
    """

    @staticmethod
    def get(request, camera_uid):
        camera = DogCamera.objects.get(uid=camera_uid)
        events = DogCameraEvent.objects.filter(camera=camera).order_by('-id')[0:30]

        camera = CurrentDogCamerasSerializer(camera, context={'request': request}).data
        events = DogCameraEventSerializer(events, context={'request': request}, many=True).data
        camera['timestamp'] = DogUpdatedTime.objects.all().first().value
        return Response({
            'status': status.HTTP_200_OK,
            'data': {
                'camera': camera,
                'events': events
            }
        })


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


class UpdateCamerasView(APIView):
    """
    Update and get cameras data
    """

    @staticmethod
    def get(request):
        session = boto3.session.Session()

        s3 = session.client(
            service_name='s3',
            endpoint_url='https://storage.yandexcloud.net',
            config=Config(signature_version=UNSIGNED)
        )

        cameras = Camera.objects.all()
        for camera in cameras:
            images = []
            for key in s3.list_objects(Bucket='reality-x', Prefix=f'trash/{camera.uid}/')['Contents']:
                if not key['Key'].lower().endswith('/'):
                    images.append(f'https://s3.yandexcloud.net/reality-x/{key["Key"]}')
            while True:
                new_last_img_name = images[random.randrange(len(images))]
                if not camera.last_img == new_last_img_name:
                    camera.last_img = new_last_img_name
                    break
            camera.save()

        cameras = Camera.objects.all()

        data = {
            "img_size": 1080,
            "conf": 0.483,
            "urls": [
                camera.last_img for camera in cameras
            ]
        }

        response = requests.post(f'{ML_ADDRESS}trash/', timeout=10000,
                                 json=data).json()
        for el in response:
            camera_uid = el['url'].split('/')[-2]
            camera = Camera.objects.get(uid=camera_uid)
            camera.last_img_pred = el['url']
            camera.save()

            camera_event = CameraEvent(
                containers_number=el['n_all'],
                filled_containers_number=el['n_full'],
                camera=camera
            )
            camera_event.save()
            camera.is_filled = el['overall']
            camera.save()
        update_time = UpdatedTime.objects.all().first()
        update_time.set_new_time()

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
        events = CameraEvent.objects.filter(camera=camera).order_by('-id')[0:30]

        camera = CurrentCamerasSerializer(camera, context={'request': request}).data
        events = CameraEventSerializer(events, context={'request': request}, many=True).data
        camera['timestamp'] = UpdatedTime.objects.all().first().value
        return Response({
            'status': status.HTTP_200_OK,
            'data': {
                'camera': camera,
                'events': events
            }
        })


class CreateUpdatedTime(APIView):
    """
    Fill database with test data
    """

    @staticmethod
    def get(request):
        if UpdatedTime.objects.all().exists():
            update_times = UpdatedTime.objects.all()
            update_times.delete()
        update_time = UpdatedTime()
        update_time.save()

        if DogUpdatedTime.objects.all().exists():
            update_times = DogUpdatedTime.objects.all()
            update_times.delete()
        update_time = DogUpdatedTime()
        update_time.save()

        return Response('true')


class CreateCameras(APIView):
    """
    Fill database with test data
    """

    @staticmethod
    def get(request):
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
                'address': "Альметьевск; Гафиатуллина 47: ТКО"
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

        if DogCamera.objects.all().exists():
            cameras = DogCamera.objects.all()
            cameras.delete()
        for el in test_cameras:
            camera = DogCamera(
                uid=el['uid'],
                address=el['address']
            )
            camera.save()

        return Response('true')


class SetCoordinates(APIView):
    """
    Fill database with test data
    """

    @staticmethod
    def get(request):
        cameras = Camera.objects.all()
        for camera in cameras:
            camera.get_coordinates()
        cameras = DogCamera.objects.all()
        for camera in cameras:
            camera.get_coordinates()
        return Response('true')
