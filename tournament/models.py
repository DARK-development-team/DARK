from django.db import models


class Queue(models.Model):
    title = models.CharField(max_length=20)
    requirements = models.CharField(max_length=500)

    def __str__(self):
        return self.title
