import random

from django.db import models
from dark.models.user.user import User


def create_new_access_key():
    return random.randint(1000, 9999)


class Tournament(models.Model):
    name = models.CharField(max_length=30, blank=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_private = models.BooleanField(default=False)
    participants = models.ManyToManyField(User, related_name='participants')
    access_key = models.IntegerField(blank=False, editable=False, default=create_new_access_key())

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'creator')
        constraints = [
            models.CheckConstraint(check=models.Q(start_date__lt=models.F("end_date")),
                                   name='tournament_start_date_lt_end_date'),
        ]
