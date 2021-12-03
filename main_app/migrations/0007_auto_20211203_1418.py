# Generated by Django 3.2.6 on 2021-12-03 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_camera_last_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='error_status',
            field=models.BooleanField(default=False, verbose_name='Ошибка'),
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
                'verbose_name': 'Событие с контейнерами',
                'verbose_name_plural': 'События с контейнерами',
            },
        ),
    ]