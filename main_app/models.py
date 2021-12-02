import sys

import requests
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models
import os

if os.getenv("BACKEND_YANDEX_MAPS_API_KEY") is not None:
    YANDEX_MAPS_API_KEY = os.getenv("BACKEND_YANDEX_MAPS_API_KEY")
else:
    print("'BACKEND_YANDEX_MAPS_API_KEY' env variable is not defined")
    sys.exit()
print('YANDEX_MAPS_API_KEY: ', YANDEX_MAPS_API_KEY)


class UpdatedTime(models.Model):
    value = models.DateTimeField('Время обновления', default=timezone.now)

    class Meta:
        verbose_name = 'Время обновления камер'
        verbose_name_plural = 'Время обновления камер'

    def __str__(self):
        return str(self.id)

    def set_new_time(self, *args, **kwargs):
        self.value = timezone.now()
        super().save(*args, **kwargs)


class Camera(models.Model):
    uid = models.IntegerField('ID камеры', blank=True, null=True)
    address = models.CharField('Адрес', max_length=500)
    x_coordinate = models.CharField('X-координата', max_length=100, blank=True)
    y_coordinate = models.CharField('Y-координата', max_length=100, blank=True)
    error_status = models.BooleanField('Ошибка', default=False)
    is_filled = models.BooleanField('Заполнен', default=False)
    last_img = models.CharField('Последний кадр', max_length=500, blank=True)

    class Meta:
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'

    def __str__(self):
        return self.address

    def get_coordinates(self, *args, **kwargs):
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
