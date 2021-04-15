from django.db import models


class Platform(models.Model):

    name = models.CharField(max_length=30, blank=False, unique=True)
    address = models.URLField(blank=False, unique=True)

    def __str__(self):
        return self.name
