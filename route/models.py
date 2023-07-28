from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        related_name="source_routes",
        on_delete=models.CASCADE
    )
    destination = models.ForeignKey(
        Airport,
        related_name="destination_routes",
        on_delete=models.CASCADE
    )
    distance = models.IntegerField()
