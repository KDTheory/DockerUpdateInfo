from django.db import models
from django.utils import timezone

class Container(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    current_version = models.CharField(max_length=255)
    docker_hub_version = models.CharField(max_length=255, blank=True, null=True)
    gist_version = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.image} - {self.current_version}"
