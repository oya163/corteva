# Generated by Django 4.0.6 on 2022-12-26 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0004_alter_yielddata_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WeatherData',
        ),
    ]
