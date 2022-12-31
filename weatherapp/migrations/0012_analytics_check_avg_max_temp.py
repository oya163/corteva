# Generated by Django 4.0.6 on 2022-12-31 03:26

from django.db import migrations, models
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapp', '0011_alter_analytics_options_alter_weatherdata_options_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='analytics',
            constraint=models.CheckConstraint(check=models.Q(('avg_max_temp__gt', django.db.models.expressions.F('avg_min_temp'))), name='check_avg_max_temp'),
        ),
    ]
