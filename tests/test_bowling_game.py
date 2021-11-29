import random


from BowlingScoringApp.tests.pytest_base import PytestBase

from BowlingScoringApp.bowling_game import BowlingGame


class TestBowlingGame(PytestBase):

    def test_create_game(self):
        bowling_game = BowlingGame()
        assert isinstance(bowling_game, object)

    def test_gutterGame(self):
        bowling_game = BowlingGame()
        number_of_frames, shots_per_frame = 2, 10
        total_shots = shots_per_frame * number_of_frames
        self.add_multiple_shots_with_same_value(bowling_game, 0, total_shots)
        assert bowling_game.score == 0

    def test_allRollsSinglePinsGame(self):
        bowling_game = BowlingGame()
        number_of_frames, shots_per_frame = 2, 10
        total_shots = shots_per_frame * number_of_frames
        self.add_multiple_shots_with_same_value(bowling_game, 1, total_shots)
        assert bowling_game.score == 20

    def test_gameHasASpareFrame(self):
        bowling_game = BowlingGame()
        self.add_spare_frame(bowling_game)
        bowling_game.add_shot(8)
        bowling_game.add_shot(1)
        number_of_frames, shots_per_frame = 2, 8
        total_shots = shots_per_frame * number_of_frames
        self.add_multiple_shots_with_same_value(bowling_game, 0, total_shots)
        assert bowling_game.score == 27

    def test_spareGame(self):
        bowling_game = BowlingGame()
        number_of_frames, shots_per_frame = 2, 10
        total_shots = shots_per_frame * number_of_frames
        self.add_multiple_shots_with_same_value(bowling_game, 5, total_shots)
        bowling_game.add_shot(5)
        assert bowling_game.score == 150

    def test_gameHasAStrikeFrame(self):
        bowling_game = BowlingGame()
        bowling_game.add_shot(10)
        bowling_game.add_shot(2)
        bowling_game.add_shot(3)
        number_of_frames, shots_per_frame = 2, 8
        total_shots = shots_per_frame * number_of_frames
        self.add_multiple_shots_with_same_value(bowling_game, 0, total_shots)
        assert bowling_game.score == 20

    def test_strikeGame(self):
        bowling_game = BowlingGame()
        number_of_frames, shots_per_frame = 2, 10
        total_shots = shots_per_frame * number_of_frames
        self.add_multiple_shots_with_same_value(bowling_game, 10, total_shots)
        bowling_game.add_shot(10)
        assert bowling_game.score == 300

    def add_multiple_shots_with_same_value(self, bowling_game, shot_value: int, number_of_shots_to_add: int) -> None:
        shots = [shot_value] * number_of_shots_to_add
        for shot in shots:
            bowling_game.add_shot(shot)

    def add_spare_frame(self, bowling_game):
        first_shot = random.randint(0, 9)
        bowling_game.add_shot(first_shot)
        bowling_game.add_shot(10 - first_shot)
