from django.db import models
from dark.models.user.user import User


class Tournament(models.Model):
    name = models.CharField(max_length=30, blank=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'creator')
        constraints = [
            models.CheckConstraint(check=models.Q(start_date__lt=models.F("end_date")),
                                   name='tournament_start_date_lt_end_date'),
        ]
