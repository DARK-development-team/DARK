from django.test import TestCase
from django.db import IntegrityError

from datetime import datetime

from ..tournament import Tournament
from dark.models.user import User


class TournamentTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')

    def test_start_date_lt_end_date(self):
        self.assertRaises(
            IntegrityError,
            Tournament.objects.create,
            name="dummy",
            creator=self.user,
            start_date=datetime.strptime("01/01/20 20:00:00", '%d/%m/%y %H:%M:%S'),
            end_date=datetime.strptime("01/01/20 19:00:00", '%d/%m/%y %H:%M:%S')
        )

    def test_tournament_str(self):
        tournament = Tournament.objects.create(
            name="dummy",
            creator=self.user,
            start_date=datetime.strptime("01/01/20 19:00:00", '%d/%m/%y %H:%M:%S'),
            end_date=datetime.strptime("01/01/20 20:00:00", '%d/%m/%y %H:%M:%S'))
        self.assertEqual(str(tournament), tournament.name)
