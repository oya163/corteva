from django.db import models


# Weather Data model
class WeatherData(models.Model):
    date = models.DateField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    precipitation = models.FloatField()
    station_id = models.CharField(max_length=11, default='USC00110072')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'weatherdata'
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
        # To prevent the duplicate insertion
        unique_together = ["date", "corn_grain_yield"]

    def __str__(self):
        return f"{self.date} {self.corn_grain_yield}"
