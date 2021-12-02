import sys

import requests
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from rest_framework.authtoken.admin import User
from django.utils import timezone
from django.db.models import Q
from django.db import models

from datetime import timedelta
from uuid import uuid4
from io import BytesIO
from PIL import Image
import os

if os.getenv("BACKEND_YANDEX_MAPS_API_KEY") is not None:
    YANDEX_MAPS_API_KEY = os.getenv("BACKEND_YANDEX_MAPS_API_KEY")
else:
    print("'BACKEND_YANDEX_MAPS_API_KEY' env variable is not defined")
    sys.exit()
print('YANDEX_MAPS_API_KEY: ', YANDEX_MAPS_API_KEY)


class Camera(models.Model):
    address = models.CharField('Адрес', max_length=500)
    x_coordinate = models.CharField('X-координата', max_length=100, blank=True)
    y_coordinate = models.CharField('Y-координата', max_length=100, blank=True)
    error_status = models.BooleanField(default=False)

    # last_img =
    # timestamp =
    # is_filled =

    # uid = models.CharField('Уникальный идентификатор', max_length=50, default='none')
    # name = models.CharField('Название', max_length=50)
    # img = models.ImageField('Изображение', upload_to='rooms/images', blank=True)
    # img_compressed_resized = models.ImageField('Изображение (сжатое)', upload_to='rooms/img_compressed_resized',
    #                                            blank=True)
    # description = models.TextField('Описание', max_length=200, blank=True)
    # icon = models.ForeignKey('Icon', on_delete=models.SET_NULL, verbose_name='Иконка',
    #                          related_name='rooms', null=True, blank=True)
    #
    # exposition = models.ForeignKey('Exposition', on_delete=models.CASCADE, verbose_name='Выставка',
    #                                related_name='rooms')
    # connected_rooms = models.ManyToManyField('self', verbose_name='Соединенные комнаты',
    #                                          related_name='root_room', blank=True)
    # is_archived = models.BooleanField('Архивирована', default=False)

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'

    def __str__(self):
        return self.address

    # def get_new_last_img(self, *args, **kwargs):
    #
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            url = "https://geocode-maps.yandex.ru/1.x"

            params = {
                'geocode': self.address,
                'apikey': YANDEX_MAPS_API_KEY,
                'format': 'json',
            }

            r = requests.get(url=url, params=params)

            coordinates = r.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point'][
                'pos'].split(' ')

            self.x_coordinate = coordinates[1]
            self.y_coordinate = coordinates[0]
            self.error_status = False
        except:
            self.y_coordinate = ''
            self.x_coordinate = ''
            self.error_status = True
        super().save(*args, **kwargs)
