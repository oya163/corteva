from django.db import models

from django.db.models import CheckConstraint, Q, F

# Weather Data model


class WeatherData(models.Model):
    date = models.DateField()
    max_temp = models.FloatField(null=True)
    min_temp = models.FloatField(null=True)
    precipitation = models.FloatField(null=True)
    station_id = models.CharField(max_length=11, default='USC00110072')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'weatherdata'
        ordering = ['id']
        # To prevent the duplicate insertion
        unique_together = ["date", "max_temp",
                           "min_temp", "precipitation", "station_id"]

    def __str__(self):
        return f"{self.date} {self.station_id} {self.precipitation}"


# Yield Data model
class YieldData(models.Model):
    date = models.DateField()
    corn_grain_yield = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'yielddata'
        ordering = ['id']
        # To prevent the duplicate insertion
        unique_together = ["date", "corn_grain_yield"]

    def __str__(self):
        return f"{self.date} {self.corn_grain_yield}"


# Analytics Data model
class Analytics(models.Model):
    date = models.DateField()
    avg_max_temp = models.FloatField(null=True)
    avg_min_temp = models.FloatField(null=True)
    total_precipitation = models.FloatField(null=True)
    station_id = models.CharField(max_length=11, default='USC00110072')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'analytics'
        ordering = ['id']
        # To prevent the duplicate insertion
        unique_together = ["date", "avg_max_temp",
                           "avg_min_temp", "total_precipitation",
                           "station_id"]

        constraints = [
            CheckConstraint(
                check=Q(avg_max_temp__gt=F('avg_min_temp')),
                name='check_avg_max_temp',
            ),
        ]

    def __str__(self):
        return f"{self.date} {self.station_id} {self.total_precipitation}"
