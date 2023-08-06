import os.path
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


def airport_image_file_path(instance, file_name):
    _, extension = os.path.splitext(file_name)
    file_name = (
        f"{slugify(instance.name)}"
        f"-{slugify(instance.closest_big_city)}"
        f"-{uuid.uuid4()}{extension}"
    )
    return os.path.join("uploads", "airports", file_name)


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    closest_big_city = models.CharField(max_length=255)
    image = models.ImageField(
        null=True, upload_to=airport_image_file_path
    )

    def __str__(self):
        return self.name

    def get_destination_names(self):
        """
        This method returns all airport
        names that user can fly from the
        current airport
        """
        return [
            route.destination.name
            for route in self.source_routes.all()
        ]


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

    class Meta:
        unique_together = ["source", "destination"]

    def clean(self):
        source = self.source_id
        destination = self.destination_id

        if source == destination:
            raise ValidationError(
                "Source name and destination cannot be the same."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
