# Generated by Django 3.2.6 on 2021-12-03 13:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_dogcameraevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='DogUpdatedTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время обновления')),
            ],
            options={
                'verbose_name': 'Собаки - Время обновления камер',
                'verbose_name_plural': 'Собаки - Время обновления камер',
            },
        ),
    ]
