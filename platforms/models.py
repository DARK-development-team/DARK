from django.db import models


class Platform(models.Model):

    name = models.CharField(max_length=30, blank=False, unique=True)
    address = models.URLField(blank=False, unique=False)
    commit = models.CharField(max_length=50)
    package_to_run = models.CharField(max_length=30)

    class Meta:
        unique_together = ('address', 'commit')

    def __str__(self):
        return self.name
