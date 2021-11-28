
from BowlingScoringApp.tests.pytest_base import PytestBase

from BowlingScoringApp.bowling_game import BowlingGame


class TestBowlingGame(PytestBase):

    def test_create_game(self):
        bowling_game = BowlingGame()
