# Generated by Django 3.2.6 on 2021-12-02 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20211202_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='last_img',
            field=models.CharField(blank=True, max_length=500, verbose_name='Последний кадр'),
        ),
    ]