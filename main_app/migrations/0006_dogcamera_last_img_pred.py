# Generated by Django 3.2.6 on 2021-12-03 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_dogupdatedtime'),
    ]

    operations = [
        migrations.AddField(
            model_name='dogcamera',
            name='last_img_pred',
            field=models.CharField(blank=True, max_length=500, verbose_name='Распознанный кадр'),
        ),
    ]
