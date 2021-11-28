
from BowlingScoringApp.tests.pytest_base import PytestBase

from BowlingScoringApp.bowling_game import BowlingGame


class TestBowlingGame(PytestBase):

    def test_create_game(self):
        bowling_game = BowlingGame()
        assert isinstance(bowling_game, object)

    def test_gutterGame(self):
        bowling_game = BowlingGame()

        shots_per_frame = 2
        number_of_frames = 10
        total_shots = shots_per_frame * number_of_frames

        shots = [0] * total_shots
        for shot in shots:
            bowling_game.add_shot(shot)

        assert bowling_game.score == 0

    def test_allRollsSinglePinsGame(self):
        bowling_game = BowlingGame()

        shots_per_frame = 2
        number_of_frames = 10
        total_shots = shots_per_frame * number_of_frames

        shots = [1] * total_shots
        for shot in shots:
            bowling_game.add_shot(shot)

        assert bowling_game.score == 20
