from django.test import TestCase
from django.db import IntegrityError

from datetime import datetime

from ..user import User
from ..tournament import Tournament, TournamentRound


class RoundModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='12345')
        cls.tournament = Tournament.objects.create(
            name="dummy",
            creator=user,
            start_date=datetime.strptime("01/01/20 18:00:00", '%d/%m/%y %H:%M:%S'),
            end_date=datetime.strptime("01/01/20 22:00:00", '%d/%m/%y %H:%M:%S')
        )

    def test_start_date_lt_end_date(self):
        self.assertRaises(
            IntegrityError,
            TournamentRound.objects.create,
            name="dummy",
            tournament=self.tournament,
            start_date=datetime.strptime("01/01/20 20:00:00", '%d/%m/%y %H:%M:%S'),
            end_date=datetime.strptime("01/01/20 19:00:00", '%d/%m/%y %H:%M:%S')
        )

    def test_start_date_ge_tournament_start_date(self):
        self.assertRaises(
            IntegrityError,
            TournamentRound.objects.create,
            name="dummy",
            tournament=self.tournament,
            start_date=datetime.strptime("01/01/20 17:00:00", '%d/%m/%y %H:%M:%S'),
            end_date=datetime.strptime("01/01/20 19:00:00", '%d/%m/%y %H:%M:%S')
        )

    def test_end_date_le_tournament_end_date(self):
        self.assertRaises(
            IntegrityError,
            TournamentRound.objects.create,
            name="dummy",
            tournament=self.tournament,
            start_date=datetime.strptime("01/01/20 21:00:00", '%d/%m/%y %H:%M:%S'),
            end_date=datetime.strptime("01/01/20 23:00:00", '%d/%m/%y %H:%M:%S')
        )
