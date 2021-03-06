# Generated by Django 3.2.6 on 2021-12-03 12:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(blank=True, null=True, verbose_name='ID камеры')),
                ('address', models.CharField(max_length=500, verbose_name='Адрес')),
                ('x_coordinate', models.CharField(blank=True, max_length=100, verbose_name='X-координата')),
                ('y_coordinate', models.CharField(blank=True, max_length=100, verbose_name='Y-координата')),
                ('error_status', models.BooleanField(default=False, verbose_name='Ошибка')),
                ('is_filled', models.BooleanField(default=False, verbose_name='Заполнен')),
                ('last_img', models.CharField(blank=True, max_length=500, verbose_name='Последний кадр')),
            ],
            options={
                'verbose_name': 'Мусор - Камера',
                'verbose_name_plural': 'Мусор - Камеры',
            },
        ),
        migrations.CreateModel(
            name='UpdatedTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время обновления')),
            ],
            options={
                'verbose_name': 'Мусор - Время обновления камер',
                'verbose_name_plural': 'Мусор - Время обновления камер',
            },
        ),
        migrations.CreateModel(
            name='CameraEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('containers_number', models.IntegerField(blank=True, null=True, verbose_name='Количество контейнеров')),
                ('filled_containers_number', models.IntegerField(blank=True, null=True, verbose_name='Количество заполненных контейнеров')),
                ('camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='main_app.camera', verbose_name='Камера')),
            ],
            options={
                'verbose_name': 'Мусор - Событие',
                'verbose_name_plural': 'Мусор - События',
            },
        ),
    ]
